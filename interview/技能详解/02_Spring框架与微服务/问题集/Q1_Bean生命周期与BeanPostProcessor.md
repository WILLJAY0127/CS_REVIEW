# Q1：Bean 实例化、属性填充、初始化为什么要拆成几步？`@Autowired` 在哪个阶段？BeanPostProcessor 能干什么，有什么限制？

> 对应技能地图：IOC/Bean 生命周期、AOP 织入时机、循环依赖三级缓存、事务失效
> 定位：本文从零基础讲到面试口述，中间穿插四个真实故障。配套学习路径见 [Q1_学习路径_从死循环到三级缓存.md](Q1_学习路径_从死循环到三级缓存.md)

---

## 零、一句话记忆锚

> 拆三步不是为了好看，是为了"**先造半成品 → 再挂依赖 → 最后包装**"，循环依赖和 AOP 代理都靠"半成品可见"成立。

---

## 一、小白地基：Bean 是什么，容器是什么

先接受三个事实，不然后面全是天书：

1. **Bean = 由容器替你 `new` 出来、并且由容器保管的对象**。你自己 `new` 的不算。
2. 容器（`ApplicationContext`）本质上是**一个工厂 + 一个仓库**：启动时把所有该造的对象造好，放进仓库，谁要用就来仓库拿。
3. 默认一个 Bean **只造一次**（单例），造好就长期放着。所以"造到一半被别人要走"这件事，才需要特殊处理。

---

## 二、一级 / 二级 / 三级缓存到底是什么（别背名字）

Spring 里这三个东西真名叫 `singletonObjects`、`earlySingletonObjects`、`singletonFactories`，业内俗称一级、二级、三级缓存。它们**不是三个装满同款对象的仓库**，级别越高，内容越不完整：

| 俗称 | 真名 | 存的是什么 | 白话 |
|---|---|---|---|
| 一级缓存 | `singletonObjects` | 完全造好的成品对象 | 成品车库，开走就能用 |
| 二级缓存 | `earlySingletonObjects` | 早期引用（可能已是代理） | 半成品区，车架焊好了，零件还没装 |
| 三级缓存 | `singletonFactories` | `ObjectFactory`（一个函数，**不是对象**） | 提货券，凭券才能去半成品区提一台 |

**最容易搞错的一点**：三级缓存存的**根本不是对象**，是一个"能生产早期引用的函数"。可以理解成一张提货券：拿着券去窗口，窗口才现场给你造一台半成品。

> 一句话：**一级放成品，二级放半成品，三级放"能生产半成品的券"**。

---

## 三、一个 Bean 的完整流水线（5 步）

用汽车装配厂的视角看 `doCreateBean` 干的事：

| 步骤 | 源码方法 | 干了什么 | 此刻对象的状态 |
|---|---|---|---|
| 1 造壳 | `createBeanInstance` | 选构造器、反射 `new` 一个空对象 | 字段全是 `null` / `0` |
| 2 登记半成品 | `addSingletonFactory` | 把"提货券"放进三级缓存 | 还是空壳，但**别人已经可以凭券拿到它** |
| 3 装零件 | `populateBean` | `@Autowired`、`@Value` 注入依赖 | 字段有值了 |
| 4 调试出厂 | `initializeBean` | `@PostConstruct` → `init-method` → 生成 AOP 代理 | 功能齐了，可能已套上代理 |
| 5 进车库 | `addSingleton` | 放进一级缓存，清掉二级三级 | 成品，全局可用 |

第 4 步内部还有细分：`Aware` 回调 → `BeanPostProcessor.before`（`@PostConstruct` 在这里被反射调用）→ `afterPropertiesSet` / `init-method` → `BeanPostProcessor.after`（**AOP 代理在这里 `wrapIfNecessary`**）。

注意第 2 步：**半成品一造出来就立刻登记**，而不是等装完零件。这个动作看起来多余，其实整个循环依赖方案全靠它。

---

## 四、为什么必须拆成几步（题眼）

不是"Spring 想拆"，是**三个硬约束逼出来的**：

1. **顺序约束**：没有对象没法填属性；依赖没填完不能跑初始化（否则 `init` 里用字段全是 null）。
2. **循环依赖约束**：只有把"造壳"和"装零件"拆开，A 才能在刚 `new` 出来、还没填充时就把 `ObjectFactory` 丢进三级缓存，让 B 填充时能拿到 A 的早期引用。合成一步，循环依赖无解。
3. **可扩展约束**：每两个阶段之间都插了钩子（实例化前后、填充前后、初始化前后），AOP 代理、`@Autowired`、`@PostConstruct` 全是挂在这些钩子上的**外挂组件**，而不是硬编码进主流程。拆开才有插槽。

### 用"两个工人"讲循环依赖

场景：Bean A 需要 B，Bean B 也需要 A（字段注入）。

如果规定"**必须完全造好才能给别人用**"：

1. 造 A，装零件时需要 B → 去造 B
2. 造 B，装零件时需要 A → A 还没造好，不能给 → 回去造 A
3. 死循环，永远造不完 → `StackOverflowError`

解法很朴素：**车架一焊好，就先登记"半成品可取"**。

1. 造 A 的空壳 → 立刻登记提货券
2. 造 A 装零件，需要 B → 去造 B
3. 造 B 装零件，需要 A → A 虽没装完，但**有券** → 凭券拿到 A 的半成品
4. B 装完出厂，A 继续装完出厂
5. A 正式进车库时，把半成品区和提货券一起清掉

---

## 五、为什么还要第三级？两级不够吗

这是整个知识点最值钱的地方。

第 4 步要给 A **套一个代理**。代理就是"替身对象"：别人调 A 的方法，实际先经过替身，替身可以在前后加逻辑（事务、缓存、日志、异步都靠它）。

B 来要 A 的半成品时，你给谁？

- **给裸的 A** → B 拿到没套替身的 A，以后 B 调 A 的方法，事务、缓存全不生效。
- **给提前套好替身的 A** → 替身必须在"半成品阶段"就造出来。可如果这个 Bean 根本没有循环依赖、压根没人提前要它，这个替身就白造了一次（造替身有成本，判断要不要造也不简单）。

于是 Spring 选第三条路：**半成品区不放东西，只放一张"提货券"**。

- 没人来提前要 → 券一直躺着，不产生任何替身，正常流程走完后统一套替身。
- 真有人来要 → 才凭券现场生成替身，并把结果放进二级缓存。

这就是三级缓存的唯一作用：**把"要不要生成代理"从"造壳时"推迟到"真被需要时"，并保证替身只造一次**（源码里用 `earlyProxyReferences` 记录，防止重复套）。

> **两级缓存就能解决循环依赖，第三级纯粹是为了 AOP 代理延迟生成、且只生成一次。**

面试被问"两级行不行"，答这句就够。

---

## 五·补、循环依赖最终长什么样：一个环，不是无限嵌套

### 一句话结论

**不是无限循环的对象，是"两个对象、一根环"。**

内存里 A 只有一个、B 只有一个，只是 A 的字段指向 B，B 的字段又指回 A。这叫**引用环（reference cycle）**，不是无限嵌套的结构。

### 长什么样

```text
堆内存（就这两个对象，再无其它）

   ┌─────────────────────┐
   │  A 实例              │
   │  b  ────────────┐    │
   └─────────────────│────┘
                     │
                     ▼
   ┌─────────────────────┐
   │  B 实例              │
   │  a  ────────────┐    │
   └─────────────────│────┘
                     │
                     └──────► 回到上面那个 A（同一个对象）
```

引用链可以一直走下去：`a.b.a.b.a.b...`，永远不会停 —— **但每一步都踩在已经存在的对象上，不会再 new 出第三个对象**。

跑道可以一直跑，但跑道长度是固定的。

### 三个"无限"必须分清

| 说法 | 是无限的吗 | 说明 |
|---|---|---|
| 对象数量 | 否 | 就 2 个（单例下永远只有 1 个 A、1 个 B） |
| 引用链长度 | 是 | `a.b.a.b...` 可无限遍历，但都在同一批对象上打转 |
| 创建过程 | 无缓存时才是死循环 | "造 A → 要 B → 造 B → 要 A → 再回来造 A → ..." 是**调用栈**无限加深，最后 `StackOverflowError` |

**三级缓存打破的是第三行 ——「创建过程的死循环」，不是第一、二行。**

### 关键：Spring 从没打算消除这个环

- **创建过程**：被打破了。A 造到一半先把提货券登记出去，B 拿到半成品继续走，A 再接着装完。
- **对象结构**：环**依然存在**，而且是永久的。最终 `A.b` 指向 B，`B.a` 指回 A。业务上本来就是互相依赖，不可能消除。

所以成品是：**两个完整对象，互相持有对方引用，一个闭环**。

验证只要一行：

```java
A a = context.getBean(A.class);
System.out.println(a.getB().getA() == a);  // true
```

`true` 说明 B 里存的 `A`，和从容器拿到的 `A`，**是同一个对象**，不是副本、不是新造的。

### 早期引用会不会"过期"

不会。B 填充时拿到的是 A 的**早期引用**（可能已是代理），但早期引用指向的就是那个对象本身 —— 半成品 = 成品，只是字段还没填满。引用不会失效，只是它指向的对象内容后来被补全了。

唯一的变化是代理场景：B 拿到代理对象时，Spring 用 `earlyProxyReferences` 保证一级缓存里最终放进去的**也是同一个代理**，不会出现"B 拿着旧代理、容器里存着新代理"的分裂。

### 这个环带来的实际后果

| 场景 | 后果 |
|---|---|
| GC 回收 | 没问题。JVM 用可达性分析而非引用计数，环能整体被回收，不内存泄漏 |
| JSON 序列化 | 会 `StackOverflowError`（Jackson 递归展开 A→B→A→…），需 `@JsonIgnore` 或 `@JsonManagedReference` |
| `toString` / `equals` / `hashCode` | 手写递归同样爆栈，Lombok `@Data` 生成的 `toString` 就会踩这个坑 |
| 设计层面 | 通常说明两个类职责耦合过度，分层没切干净 |

### 设计层面：循环依赖为什么是一个"信号"

这是这道题最容易被忽略、但在工程上最值钱的一层。

**能跑起来 ≠ 设计正确。** 三级缓存的职责是让步履蹒跚的系统先开机，不是给坏设计发许可证。Spring 官方本身也不推荐依赖它，Spring Boot 2.6 起 `spring.main.allow-circular-references` 默认就是 `false`，等于在说：**能启动，但请你自己看看是不是设计有问题。**

怎么判断这个环是"合理"还是"坏"：

| 形态 | 判断 | 处理 |
|---|---|---|
| Service A ⇄ Service B，各自持有对方 Bean | 坏环 | 拆：公共逻辑下沉到第三个类，或让 B 只依赖 Repository |
| A 需要 B 的**数据**，B 需要 A 的**数据** | 坏环 | 把数据获取下沉到 DAO / 领域层，或由调用方把参数传进来 |
| A 调 B 后需要 B 反过来通知 A | 坏环（回调式） | 改成事件 / 监听器（`ApplicationEventPublisher`），把"通知"从"依赖"里剥离 |
| JPA 实体的 `@OneToMany` ⇄ `@ManyToOne` | 合理 | 这是**持久化映射**的双向关联，不是 Bean 依赖注入，不受此限 |
| 框架基础设施（如某些 BPP 与容器自身） | 合理 | 框架层需要互指，属于受控特例 |

拆环的四个常用手段，按优先级：

1. **下沉**：把双方都需要的查询/计算抽到第三个类（如 `XxxQueryService` 或 Repository），A、B 各自只依赖它，不再互相依赖。
2. **上移编排**：把"A 调 B、B 又调 A"的流程交给更上层的编排者（Controller 或 Application Service），两边都变成单向调用。
3. **事件解耦**：真正需要"反向通知"时，用事件发布/订阅替代直接方法调用。
4. **参数传递**：A 只是要 B 手里的某个对象，就别注入整个 B，让调用方把对象作为参数传进来。

一句话收口：

> **循环依赖不是"Spring 帮你兜住了所以没关系"，而是"结构上两个人互相攥着对方的把柄"。能启动只是暂时没打架，业务一复杂就会变成改不动的地方。**

### 类比收口

> 循环依赖不是"无限个盒子套无限个盒子"。
> 是**两张纸，各自写着对方的电话号码**。纸只有两张，但你可以顺着号码来回打，永远打不完。

Spring 做的事，是让"写号码"这件事能顺利完成 —— 而不是把号码擦掉。

---

## 六、`@Autowired` 到底在哪一步

- **字段注入 / setter 注入**：在**第 3 步属性填充**（`populateBean`）里，由 `AutowiredAnnotationBeanPostProcessor` 解析并赋值。
- **构造器注入**：是特例，发生在**第 1 步实例化**（`determineCandidateConstructors` / `autowireConstructor`）。

由此直接解释两个经典坑：

1. **构造函数里读 `@Autowired` 字段是 `null`** —— 装零件还没开始。
2. **构造器互相注入启动报 `BeanCurrentlyInCreationException`** —— 造壳时就必须完整交出对方，可对方连壳都没造，没有半成品可给。**构造器注入的循环依赖，三级缓存也救不了。**

---

## 七、BeanPostProcessor 是什么、能干什么、限制在哪

**定义**：容器在"初始化之前"和"初始化之后"留的两个回调钩子。它不是给某个 Bean 专用的，而是对容器里**所有 Bean** 生效的"通用加工站"。

**能干什么**：

- 初始化前：改属性、做校验、打日志、埋点
- 初始化后：**返回一个新对象替换原对象** —— AOP 代理就是这么来的（`AbstractAutoProxyCreator` 在 after 阶段 `wrapIfNecessary`）
- 工程上：字段脱敏、多数据源切换、注册中心自动注册、自定义 starter

**子接口的分工**：

| 类型 | 能插手的位置 |
|---|---|
| `BeanPostProcessor` | 初始化前 / 后 |
| `InstantiationAwareBeanPostProcessor` | 实例化前后、属性填充前后 |
| `SmartInstantiationAwareBeanPostProcessor` | 预测类型、暴露早期引用（循环依赖关键） |
| `MergedBeanDefinitionPostProcessor` | 合并 BeanDefinition、缓存注入元数据 |

**限制（面试加分点）**：

1. **只管自家孩子**：只对当前容器创建的对象生效，你自己 `new` 的、别处传进来的，都不管。
2. **改不了"图纸"**：想改 Bean 定义（换实现类、改作用域），得用 `BeanFactoryPostProcessor`。
3. **前后位置有讲究**：`before` 阶段拿到的是裸对象，**还没有代理**；`after` 返回的才是最终对外的东西。
4. **默认排队无序**：想控制顺序得实现 `Ordered` / `PriorityOrdered` 或加 `@Order`。
5. **它自己是"最早进场的人"**：注入业务 Bean 会逼对方提前创建，打乱初始化顺序，甚至让代理还没就绪。
6. **它是全局广播**：对所有 Bean 生效，写通用逻辑必须判断类型，否则误伤一片。

---

## 八、四个真实故障详解

### 故障 1：构造函数里读 `@Autowired` 字段是 `null`

```java
@Service
public class OrderService {
    @Autowired private UserDao userDao;   // 字段注入

    public OrderService() {
        System.out.println(userDao);      // null，用的时候直接 NPE
    }
}
```

- **根因**：字段注入在第 3 步属性填充，构造函数属于第 1 步实例化。构造执行时字段还是默认值。
- **怎么确认**：构造函数、`@PostConstruct`、`afterPropertiesSet` 各打一行日志打印字段，`null → 有值 → 有值`，顺序一目了然。
- **怎么修**：
  1. **首选**改构造器注入（`private final UserDao userDao` + 构造器），依赖在造壳时就到位。
  2. 必须字段注入就把"用依赖"的逻辑挪到 `@PostConstruct` 或 `afterPropertiesSet`。
- **面试一句话**：字段注入在属性填充阶段，构造函数在实例化阶段，先后顺序决定了构造里一定拿不到。

### 故障 2：两个 Bean 构造器互相注入，启动直接失败

```java
@Service public class A { public A(B b) {} }
@Service public class B { public B(A a) {} }
```

- **现象**：启动报 `BeanCurrentlyInCreationException: Is there an unresolvable circular reference?`
- **根因**：构造器注入在第 1 步。造 A 的壳必须完整交出 B，造 B 的壳又必须完整交出 A；此时 A 连壳都没有，三级缓存里没有任何东西可暴露。
- **怎么确认**：看异常栈里的 beanName，再看该类的构造器参数，一眼定位。
- **怎么修**：
  1. **正解是重构**：把共同逻辑抽成第三个 Bean C，A→C、B→C，环就断了。
  2. `@Lazy`：在其中一个构造器参数上加 `@Lazy`，注入延迟代理，真正调用时才创建。
  3. `ObjectProvider<B>`：参数改成 `ObjectProvider`，用时 `getObject()`。
  4. **注意**：很多人说"改成字段注入就好了"。这在老版本成立，但 **Spring Boot 2.6 之后 `spring.main.allow-circular-references` 默认 false**，字段注入的循环依赖也会直接启动失败，不能当通用解。
- **面试一句话**：构造器注入在实例化阶段，没有半成品可暴露，三级缓存无效；能救的只有属性填充型循环依赖，而且新版本默认还禁止了。

### 故障 3：`@PostConstruct` 里调本类 `@Transactional` 方法，事务不生效

```java
@Component
public class OrderInitializer {
    @PostConstruct
    public void init() {
        this.loadCache();          // loadCache 上有 @Transactional
    }
    @Transactional
    public void loadCache() { /* 写库 */ }
}
```

- **根因有两层，很多资料只讲一层**：
  1. **代理还没生成**：`@PostConstruct` 在 `BeanPostProcessor.before` 执行，AOP 代理在 `after` 才 `wrapIfNecessary`，此刻 `this` 是裸对象。
  2. **就算代理生成了，`this.loadCache()` 也不走代理**：这是"自调用失效"，`this` 指向原始对象，不过代理。
- **怎么确认**：在 `loadCache` 里打印 `this.getClass().getName()`，出现 `$Proxy` 或带 `$$` 的 CGLIB 类名才说明走代理；同时开 `logging.level.org.springframework.transaction=DEBUG`，看不到事务创建日志就是没进拦截器。
- **怎么修**（按推荐度）：
  1. **把初始化动作挪出 `@PostConstruct`**：用 `ApplicationRunner` / `CommandLineRunner`，或 `@EventListener(ApplicationReadyEvent.class)`，这时容器全部就绪、代理早已生成。
  2. `SmartInitializingSingleton#afterSingletonsInstantiated`，在所有单例初始化完之后触发。
  3. **拆到另一个 Bean**：注入 `CacheLoader` 再调它，跨 Bean 调用天然经过代理。
  4. 必须在 init 里做：注入自己的代理（`@Lazy @Autowired private OrderInitializer self;` 然后 `self.loadCache()`），能用但绕。
- **面试一句话**：`@PostConstruct` 早于代理生成，`this` 是裸对象；再加上自调用本来就不走代理，两层原因叠加，事务一定失效。

### 故障 4：BeanPostProcessor 注入了业务 Bean，导致对方提前初始化

```java
@Component
public class MyBpp implements BeanPostProcessor {
    @Autowired private OrderService orderService;   // 危险写法
}
```

- **现象**：某个业务 Bean 的 `@PostConstruct` 在容器远没准备好时执行，里面用到的其他 Bean 还是 null，直接 NPE；或者启动顺序日志完全对不上；更隐蔽的是——**这个 Bean 的事务/缓存代理没生效**。
- **根因**：BPP 是在 `refresh()` 的 `registerBeanPostProcessors` 阶段创建的一批"极早期 Bean"，比普通单例早得多。它一旦注入业务 Bean，就逼着对方提前走完整条生命周期。更糟的是：**此时可能还有别的 BPP 没注册完**（比如 AOP 的 `AnnotationAwareAspectJAutoProxyCreator`），提前创建的 Bean 会被"漏加工"，代理就没了。
- **怎么确认**：
  - 所有 `@PostConstruct` 打时间戳日志，看谁先跑；顺序异常基本就能锁定。
  - 在 BPP 构造器里打断点，看调用栈是不是在 `registerBeanPostProcessors` 里。
- **怎么修**：
  1. BPP 里**不要注入业务 Bean**，改成实现 `ApplicationContextAware`，存下 `ApplicationContext`，真正需要时再 `getBean`。
  2. 或者用 `ObjectProvider<T>`，延迟到用时才取。
  3. 需要"容器全部就绪后再处理业务"的逻辑，放到 `SmartInitializingSingleton` 或 `ApplicationListener<ContextRefreshedEvent>`。
- **面试一句话**：BPP 是极早期 Bean，注入业务 Bean 会让对方提前初始化，还可能错过尚未注册的其他 BPP，导致代理缺失——这是它最隐蔽的限制。

### 四个故障对应到流水线的位置

| 故障 | 卡在第几步 | 一句话根因 |
|---|---|---|
| 构造里字段为 null | 1 实例化 | 装零件在造壳之后 |
| 构造器循环依赖失败 | 1 实例化 | 没有半成品可暴露 |
| `@PostConstruct` 事务失效 | 4 初始化（before） | 代理在 after 才生成 + 自调用 |
| BPP 注入业务 Bean | 容器启动阶段 | 太早进场，逼别人提前出生 |

---

## 九、排查工具箱

在所有关键节点打一行日志，顺序就出来了：

```java
public A()                { log.info("1 构造"); }
@PostConstruct void p()   { log.info("3 @PostConstruct"); }
void afterPropertiesSet() { log.info("4 afterPropertiesSet"); }
```

再打开 `logging.level.org.springframework.beans=TRACE`，搜 `Creating instance of bean`、`Initializing bean`、`Finished creating instance` 这几个关键词，就能在日志里看到每个 Bean 走到哪一步。

断点建议：在 `DefaultSingletonBeanRegistry#getSingleton` 打断点，条件设成目标 beanName，Evaluate 里依次看 `singletonObjects`、`earlySingletonObjects`、`singletonFactories` 三个 map 的 key，能直观看到半成品何时登记、何时升级、何时清空。

**遇到上面四类问题，先对照阶段图，基本不用猜。**

---

## 十、30 秒口述版

> 一个 Bean 从类变成可用对象要经过五步：实例化、登记半成品、属性填充、初始化、进成品缓存。拆开的核心原因是循环依赖：只有把"造壳"和"装零件"分开，才能在半成品阶段暴露引用，让回头依赖的 Bean 拿到它。
> `@Autowired` 字段注入发生在属性填充阶段；构造器注入是特例，在实例化阶段，所以构造器循环依赖救不了。
> 三级缓存里存的不是对象，是 `ObjectFactory`。两级其实就能打破循环依赖，第三级是为了 AOP 代理延迟生成、且只生成一次。
> BeanPostProcessor 是容器级的初始化前后回调，可以在 after 阶段返回代理替换原对象；限制是只管本容器创建的 Bean、改不了 BeanDefinition、before 阶段拿不到代理、默认无序、且它太早进场容易导致 Bean 提前初始化。

---

## 十一、加分点与必被追问

1. **两级缓存够不够？** 够打破循环依赖；第三级为 AOP 代理延迟生成 + 只生成一次。
2. **构造器循环依赖为什么失败？** 造壳时就要完整依赖，没有半成品可暴露。
3. **`@PostConstruct` 和 `afterPropertiesSet` 谁先？** `@PostConstruct` 先（在 before 回调里被反射调用）。
4. **`@PostConstruct` 里调本类 `@Transactional` 为什么没事务？** 代理还没生成，`this` 是裸对象。
5. **Spring Boot 2.6 后为什么循环依赖直接启动失败？** `allow-circular-references` 默认 false，官方认为循环依赖本身就是设计问题。
6. **`@Autowired` 注入的到底是代理还是原对象？** 取决于对方 Bean 是否已完成初始化：正常依赖拿到的是成品（可能是代理），循环依赖下拿到的是早期引用（可能也是提前生成的代理）。

---

## 十二、下一步怎么学

按这条顺序走，别跳：

| 层 | 内容 | 判断"可以往下走"的标准 |
|---|---|---|
| L0 | 会用：`@Autowired`、`@PostConstruct`、`InitializingBean` 谁先谁后 | 能不查资料说出顺序 |
| L1 | **主干**：`createBeanInstance → populateBean → initializeBean` | 能凭记忆画出五步流水线 |
| L2 | **循环依赖 + 三级缓存** | 能解释"为什么两级不够" |
| L3 | AOP 代理与事务失效 | 能解释 `@PostConstruct` 里事务为什么失效 |
| L4 | `refresh()` 全流程、BeanDefinition 解析 | 面试基本不考，先放着 |

具体实验步骤与手写 mini 容器代码，见 [Q1_学习路径_从死循环到三级缓存.md](Q1_学习路径_从死循环到三级缓存.md)。
