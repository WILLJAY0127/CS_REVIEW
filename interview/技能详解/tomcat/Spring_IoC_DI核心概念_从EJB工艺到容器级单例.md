# Spring IoC/DI 核心概念梳理：从 EJB 工艺到容器级单例

> 本文把四个紧密相关的问题串成一条认知链：Tomcat 是什么 → IoC 为何出现 → EJB 与 Spring 的工艺差异 → POJO/Bean 工厂/单例的精确语义。与同目录 [JAR_WAR_EAR与Tomcat_Spring_Boot关系梳理.md](file:///d:/myfile/CS_REVIEW/interview/技能详解/tomcat/JAR_WAR_EAR与Tomcat_Spring_Boot关系梳理.md)（讲打包与部署模型）配套：那篇讲**物怎么装**，本篇讲**对象怎么装**。

## 8+1 总览卡

1. **Tomcat 是纯 Java 程序**：`startup` 脚本本质是 `java org.apache.catalina.startup.Bootstrap`，Tomcat 进程 = JVM 进程；内嵌 Tomcat 不是另一种 Tomcat，只是同一份字节码改用为 Maven 依赖。
2. **IoC 不突兀**：思想原型是 1988 年好莱坞原则"Don't call us, we'll call you"，2003 年被 Spring 框架化，2004 年 Martin Fowler 定型 DI 术语，2009 年成 JSR 330 标准，2010 年 EE 自己吸收为 CDI。
3. **EE 自己就有 DI**：EJB 3.0 的 `@EJB` 注入、EE 6 的 CDI（`@Inject`/`@ApplicationScoped`）——Spring 团队直接参与了 JSR 330 制定。"Spring 发明 DI 给 EE 打补丁"是错觉。
4. **Spring 替代的是工艺不是能力**：EJB 用"接口约束 + XML 部署描述符 + 容器实例池"；Spring 用"POJO + 注解 + 反射 + 动态代理"。事务、装配、生命周期、安全这几件事两边都做，只是接入重量差一个数量级。
5. **POJO 的判据是"脱掉框架能不能活"**：不 `extends`/`implements` 框架类型，删光注解类仍能编译运行。现代宽松版允许加 `@Component` 等注解，因为注解不绑架类结构。
6. **Bean 工厂 = GoF 工厂 + 反射 + 配置 + 默认单例**：`BeanFactory` 接口核心只有 `getBean`，实现类用反射读 XML/注解装配对象，再存进 Map 缓存。
7. **DI 不强制单例**：DI 解决"装配"，单例是"复用策略"，两者正交。Spring 默认 singleton、CDI 默认 `@Dependent`、Guice 默认 prototype——规范层没有任何强制。
8. **Spring singleton ≠ GoF Singleton**：前者单例性来自容器 Map（每个 ApplicationContext 一份），后者来自类的 `static` 字段 + 私有构造（每个 ClassLoader 一份）。Spring 把单例性从"类的设计问题"挪到"容器的管理问题"，由此解放测试、替换、配置、销毁四件事。

**一句话主线**：Spring 的全部革命可以归结为一次"责任转移"——把对象创建、依赖装配、横切织入、单例管理这些责任**从业务类身上（EJB 接口绑架、GoF 静态自管）转移到容器身上（反射装配、Map 缓存、代理织入）**，业务类由此回归 POJO。

***

## 目录

1. [Tomcat 的物理身份：一个跑在 JRE 上的 Java 程序](#一tomcat-的物理身份一个跑在-jre-上的-java-程序)
2. [IoC 出现的脉络：它不突兀，EE 也需要它](#二ioc-出现的脉络它不突兀ee-也需要它)
3. [工艺替代：从"EJB 接口 + 部署描述符"到"POJO + 注解 + 反射"](#三工艺替代从-ejb-接口--部署描述符到-pojo--注解--反射)
4. [一棵树上的两条枝：Spring 与 CDI 的共性与差异](#四一棵树上的两条枝spring-与-cdi-的共性与差异)
5. [POJO 的精确定义](#五pojo-的精确定义)
6. [单例 Bean 工厂的演进](#六单例-bean-工厂的演进)
7. [DI 一定要单例么：scope 是独立维度](#七di-一定要单例么scope-是独立维度)
8. [Spring singleton 与 GoF Singleton 的本质差异](#八spring-singleton-与-gof-singleton-的本质差异)
9. [认知链总收束](#九认知链总收束)
10. [权威锚点](#十权威锚点)

***

## 一、Tomcat 的物理身份：一个跑在 JRE 上的 Java 程序

### 1. 启动脚本在做什么

`apache-tomcat/bin/startup.sh`（或 `.bat`）拆开后，核心就是一条 java 命令：

```bash
java -classpath "$CATALINA_HOME/bin/bootstrap.jar:..." \
     org.apache.catalina.startup.Bootstrap start
```

Tomcat 是**纯 Java 实现**，发行版 = 一堆 jar + 启动脚本，必须有 JRE 才能运行。Tomcat 进程本质就是一个 JVM 进程。

### 2. 三个直接推论

| 推论 | 含义 |
|---|---|
| Tomcat 进程 = JVM 进程 | 吃内存、走 GC、受 safepoint 影响，与普通 Java 服务无差别 |
| Tomcat 启动 = 启动一个 Java 应用 | `-Xmx`、`-Xlog:gc` 等 JVM 参数对它完全有效 |
| Tomcat 的类是普通 Java 类 | 这是"内嵌 Tomcat"可行的根——普通类自然能当 Maven 依赖用 |

### 3. 独立模式与内嵌模式跑的是同一份字节码

| 维度 | 独立模式 | 内嵌模式（Spring Boot） |
|---|---|---|
| 谁提供 main 入口 | Tomcat 的 `Bootstrap.main` | 应用自己的 `@SpringBootApplication.main` |
| Tomcat 类怎么加载 | Tomcat 自带的多 ClassLoader 分层 | 跟业务类一起由 Spring Boot Loader 加载 |
| 监听端口/解析 HTTP 的代码 | `org.apache.catalina.*` / `org.apache.coyote.*` | **完全相同** |

内嵌不是重写，只是把同样的类从"独立产品形态"改用为"库依赖形态"。

### 4. Tomcat 为何自带 ClassLoader 分层

独立 Tomcat 要在**同一个 JVM 里跑多个 webapp** 并支持热部署，需要让每个 webapp 的类互不干扰、卸载时可被 GC，才设计了 Common/Catalina/Shared/WebApp 多层 ClassLoader。Spring Boot 内嵌模式通常只跑一个 webapp，这一分层的必要性大幅弱化。

***

## 二、IoC 出现的脉络：它不突兀，EE 也需要它

### 1. 一个常见错觉

"DI 是 Spring 发明的、专门补 EE 的缺"——**不成立**。EE 自己就有 DI，而且 Spring 团队参与了 DI 标准制定：

| 时间 | 事件 |
|---|---|
| 2006，Java EE 5 | EJB 3.0 引入 `@EJB`，做容器管理注入 |
| 2009，JSR 330 | Spring 与 Google Guice 团队**共同提交** DI 标准注解（`@Inject`/`@Named`/`@Provider`/`@Qualifier`） |
| 2010，Java EE 6 | **CDI**（Contexts and Dependency Injection）正式纳入 EE，参考实现为 JBoss Weld |

### 2. DI 解决的根本问题：对象 A 要用对象 B 怎么办

```java
// 方案1：A 自己 new B —— 与具体实现死耦合，无法换实现、无法测试
class A { private B b = new BImpl(); }

// 方案2：A 主动查找 B（JNDI / Service Locator）—— 依赖容器，单测要 mock 容器
class A {
    private B b = (B) ctx.lookup("java:comp/env/bService");
}

// 方案3：外部把 B 塞给 A（Dependency Injection）—— A 不依赖任何容器
class A {
    private final B b;
    public A(B b) { this.b = b; }   // 谁创建 A，谁负责传 B
}
```

第三种就是 DI。它不是为 EE 设计的，而是**任何复杂 OO 系统最终都会推导出的解法**——因为前两种在"换实现"和"写单测"两个维度都走不通。

### 3. IoC 的完整血脉

| 年份 | 事件 |
|---|---|
| 1988 | 好莱坞原则"Don't call us, we'll call you"被引入软件设计——IoC 思想原型 |
| 1996 | Stefan Johnson 在 Apple Framework 中提出"Inversion of Control"一词 |
| 2000 | Apache Avalon 等早期 IoC 容器出现 |
| 2003 | PicoContainer、HiveMind 活跃；**Spring Framework 1.0 发布** |
| 2004 | Martin Fowler《Inversion of Control Containers and the Dependency Injection pattern》把 IoC 拆为 DI 与依赖查找，术语定型 |
| 2006 | Google Guice 1.0，类型安全注入 |
| 2009 | JSR 330，DI 注解标准化 |
| 2010 | CDI 1.0 进入 Java EE 6 |

### 4. EE 是否"一定需要"DI

不是语言层面的必须，但**企业级复杂系统最终都需要某种"组件装配 + 生命周期 + 配置外部化 + 容器外可测"机制**。证据是 EE 自己最后也长出了 CDI：
- 几百个组件互相协作，不能靠 `new` 拼装；
- 事务、安全等横切关注点必须统一管；
- 数据源、超时、MQ 地址必须外部化；
- 单元测试必须能在容器外秒级跑。

EJB 早期用"容器托管 + 部署描述符"满足这些需求但接口重、测试难；Spring 用 IoC + AOP 满足同样需求但接口轻、测试友好。**两者解决的是同一组问题，工艺不同。**

***

## 三、工艺替代：从"EJB 接口 + 部署描述符"到"POJO + 注解 + 反射"

### 1. 同一业务在两种范式下的对比

业务：一个下单服务，要事务、调库存、记日志。

**EJB 2.x 范式——四个文件**：

```java
// 文件1：Home 接口（创建/查找 Bean）
public interface OrderServiceHome extends EJBHome {
    OrderService create() throws RemoteException, CreateException;
}

// 文件2：Remote 接口（业务方法对外契约）
public interface OrderService extends EJBObject {
    void placeOrder(Order o) throws RemoteException;
}

// 文件3：Bean 类（被迫实现 SessionBean 的 5 个生命周期方法）
public class OrderServiceBean implements SessionBean {
    private SessionContext ctx;
    public void setSessionContext(SessionContext c) { this.ctx = c; }
    public void ejbCreate() { }
    public void ejbRemove() { }
    public void ejbActivate() { }
    public void ejbPassivate() { }

    public void placeOrder(Order o) { /* 业务 */ }
}
```

```xml
<!-- 文件4：ejb-jar.xml 部署描述符 -->
<session>
  <ejb-name>OrderService</ejb-name>
  <home>com.x.OrderServiceHome</home>
  <remote>com.x.OrderService</remote>
  <ejb-class>com.x.OrderServiceBean</ejb-class>
  <session-type>Stateless</session-type>
  <transaction-type>Container</transaction-type>
</session>
```

**Spring 范式——一个文件**：

```java
@Service
@Transactional
public class OrderService {

    @Autowired
    private InventoryService inventory;

    public void placeOrder(Order o) {
        inventory.deduct(o);
    }
}
```

### 2. EJB 工艺的五个具体痛点

- **接口绑架**：必须 `implements SessionBean`，被迫写 5 个与业务无关的空方法；
- **四份强耦合**：改一个方法名要同步改 Home/Remote/Bean/XML，漏一处部署失败；
- **容器依赖绑架**：`SessionContext` 由容器注入，`new OrderServiceBean()` 直接 NPE，无法脱离容器；
- **XML 脆弱**：描述符与类分离，IDE 不报错，部署时才暴露；
- **测试不可能**：要打包部署到应用服务器，启动 30 秒，写不出秒级单测。

### 3. 三处"换"的精确位置

| 维度 | EJB 工艺 | Spring 工艺 |
|---|---|---|
| 组件模型 | `implements SessionBean`，生命周期被容器绑架 | 普通 POJO，不实现任何框架接口 |
| 装配方式 | XML 部署描述符写死 Bean 元数据 | `@Service`/`@Autowired` 注解（或 `@Bean` 方法），容器扫描装配 |
| 创建方式 | 容器通过 Home 接口反射创建 + 实例池 | 反射直接 `clazz.getDeclaredConstructor().newInstance()` |
| 横切接入 | XML 中 `transaction-type=Container`，容器拦截 | `@Transactional` 注解 + **动态代理**织入 |
| 依赖注入 | `@EJB` | `@Autowired`（反射 `Field.set`） |
| 依赖查找 | JNDI `ctx.lookup(...)` | `ApplicationContext.getBean(...)` |
| 可测性 | 必须部署到容器 | `new` + mock 即可测 |

### 4. "反射"在 Spring 内部的物理动作

```java
// Spring 容器启动时的简化骨架
Class<?> clazz = Class.forName("com.x.OrderService");        // 反射加载
Object instance = clazz.getDeclaredConstructor().newInstance(); // 反射实例化

Field f = clazz.getDeclaredField("inventory");              // 反射拿字段
f.setAccessible(true);                                       // 突破 private
f.set(instance, inventoryBean);                              // 反射注入

// 事务靠动态代理（JDK Proxy 或 CGLIB）
OrderService proxy = (OrderService) Proxy.newProxyInstance(
    classLoader,
    new Class[]{OrderService.class},
    (p, method, args) -> {
        TransactionStatus tx = txManager.begin();
        try {
            Object ret = method.invoke(instance, args);      // 反射调真实方法
            txManager.commit(tx);
            return ret;
        } catch (Exception e) {
            txManager.rollback(tx);
            throw e;
        }
    }
);
```

"POJO + 注解 + 反射"的物理含义：
- **POJO**：类不实现任何框架接口，纯业务；
- **注解**：容器扫描时识别为装配指令；
- **反射**：运行期 `Class.forName` / `Field.set` / `Method.invoke` 完成创建、注入、代理织入。

EJB 也用反射，但把"组件必须实现什么接口"写死在规范里导致类被绑架；Spring 把"组件是什么"的决定权还给开发者。

### 5. 工艺替代全景

```
EJB 工艺                       Spring 工艺
──────────────────             ──────────────────
EJBHome / Remote 接口     →    无（普通 POJO）
implements SessionBean    →    无（不实现框架接口）
ejb-jar.xml               →    @Component / @Service（或 @Bean）
transaction-type=Container →  @Transactional（动态代理织入）
@EJB 注入                  →    @Autowired（反射 Field.set）
JNDI lookup               →    ApplicationContext.getBean
部署到外置应用服务器       →    放进 Spring 容器（可独立运行）
无法脱离容器测试           →    new + mock 即可测
```

**能力相同，工艺完全不同**：事务、装配、生命周期、安全两边都做；Spring 轻、可测、可独立运行。

***

## 四、一棵树上的两条枝：Spring 与 CDI 的共性与差异

### 1. 共性（"同一棵树"成立的理由）

| 维度 | Spring | CDI / EE |
|---|---|---|
| 解决的根本问题 | 对象图装配、横切管理、配置外部化 | 同 |
| 核心思想 | IoC + AOP | IoC + 拦截器 |
| 标准化 | 参与制定 JSR 330 | 直接消费 JSR 330 |
| 最终范式 | POJO + 注解 + 容器 | POJO + 注解 + 容器 |

代码层面已经几乎同形：

```java
// Spring
@Service
public class OrderService {
    @Autowired private InventoryService inv;
}

// CDI
@RequestScoped
public class OrderService {
    @Inject private InventoryService inv;
}
```

### 2. 三个不能被"只是实现不同"掩盖的差异

**差异 A：起点不同**
- Spring 是独立产品（2003），先有产品后影响标准；
- CDI 是 EE 规范（2010），是 EE 对 Spring 的回应。

**差异 B：覆盖范围不同**
- Spring 走纵向整合：IoC、AOP、事务、JDBC、Web MVC、Security、Cloud 全栈自己干；
- CDI 只覆盖 DI + 上下文（Request/Session/Conversation）+ 拦截器，Web/持久化/消息靠 EE 其他规范补齐。

**差异 C：部署哲学不同**
- Spring Boot：应用厚、容器薄，一个可执行 jar 一个进程；
- CDI（在 WildFly 等服务器里）：应用薄、容器厚，多应用共享外置服务器进程。

### 3. 关系图

```
              复杂对象装配 + 横切管理（共同根问题）
                        │
       ┌────────────────┴────────────────┐
       │                                 │
  Spring 路径                       CDI/EE 路径
       │                                 │
  独立产品，2003                    规范，2010 回应
  自己定 API                         消费 JSR 330
       │                                 │
  POJO + @Autowired + 反射        POJO + @Inject + 反射
  + 纵向整合全栈                   + 仅 DI/上下文/拦截器
  + 内嵌容器（Boot）               + 外置应用服务器
       │                                 │
  Spring Boot 可执行 jar           WildFlow + CDI 容器
```

**结论**："实现方式不同"成立，但要补半句——起点、范围、部署哲学也不同。两根枝都长在"DI 思想之树"上，Spring 从地下独立长出，CDI 是 EE 那棵树后来回应长出的一段。

***

## 五、POJO 的精确定义

### 1. 词源

**POJO = Plain Old Java Object**，2000 年由 Martin Fowler、Rebecca Parsons、Josh Mackenzie 造出，用来反对当时 J2EE 把业务类绑架到 EJB/Struts 框架接口的风气。

原始定义：**一个不被任何框架接口、超类绑架的、只属于 `java.lang.Object` 的 Java 对象**。

### 2. 判定标准（强 → 宽松）

| 标准 | 严格版 | 现代宽松版 |
|---|---|---|
| 继承 | 不 `extends` 任何框架类 | 不强制 extends 业务基类之外的东西 |
| 接口 | 不 `implements` 任何框架接口 | 允许标记接口 |
| 注解 | 不加任何框架注解 | 加 `@Component`/`@Inject` 仍算 POJO（注解只是元数据，不强制行为） |

注解版被接受的理由：**删掉注解类仍能编译**——注解不绑架类结构，与"必须 implements 框架接口"有本质区别。

### 3. 一个朴素判据："脱掉框架能不能活"

```java
// ✅ 严格 POJO
public class Order {
    private String id;
    private List<Item> items;
    public void addItem(Item i) { items.add(i); }
}

// ✅ 注解版 POJO（删光注解仍可编译运行，只是没人装配）
@Service
public class OrderService {
    @Autowired private InventoryService inv;
    public void placeOrder(Order o) { inv.deduct(o); }
}

// ❌ 不是 POJO：必须实现框架接口 + 5 个空方法，脱离容器无法编译运行
public class OrderServiceBean implements SessionBean {
    public void ejbCreate() { }
    public void setSessionContext(SessionContext ctx) { }
    public void ejbActivate() { }
    public void ejbPassivate() { }
    public void ejbRemove() { }
}

// ❌ 不是 POJO：必须继承框架类
public class LoginAction extends org.apache.struts.action.Action { ... }
```

**POJO 的本质不是"什么都没有"，而是"不依赖框架的身份绑定"**。框架是装配工具，不是身份标签。

### 4. POJO 的工程价值

| 价值 | 含义 |
|---|---|
| 可测 | 不依赖容器，直接 new |
| 可移植 | 可在 Spring 与 CDI 之间搬迁 |
| 可演进 | 框架升级/替换，业务类不动 |
| 可理解 | 不用先学框架就能读业务代码 |

Spring/CDI 革命的口号就是"让业务回归 POJO"。

***

## 六、单例 Bean 工厂的演进

### 1. 时间线

| 年份 | 产物 | 解决什么 |
|---|---|---|
| 1994 | GoF《设计模式》，工厂模式 | 用工厂方法解耦对象创建 |
| 2002 | 《Expert One-on-One J2EE Design and Development》 | 提出"工厂 + 配置装配 POJO" |
| 2003 | Spring 1.0，**`BeanFactory`** 成为核心接口 | 单例 Bean 工厂落地 |
| 2004 | Fowler 定型 DI 术语 | 行业语言统一 |
| 2006 | Spring 2.0，`ApplicationContext` 成主流 | 单例工厂成熟 |
| 2010 | CDI 1.0 进入 EE 6 | "容器管单例"成行业共识 |

### 2. 演进三步曲

**第一步：GoF 手工工厂**

```java
public class OrderServiceFactory {
    public OrderService create() {
        InventoryService inv = new InventoryService();
        return new OrderService(inv);
    }
}
```

问题：依赖关系硬编码在工厂里，换实现要改工厂代码。

**第二步：配置驱动的反射工厂（Rod Johnson 提议的原型）**

```java
public class BeanFactory {
    private final Map<String, Object> beans = new HashMap<>();

    public BeanFactory(XmlConfig config) throws Exception {
        for (BeanDef def : config) {
            Object bean = Class.forName(def.getClassName())
                               .getDeclaredConstructor().newInstance();
            for (Property p : def.getProperties()) {
                Field f = bean.getClass().getDeclaredField(p.getName());
                f.setAccessible(true);
                f.set(bean, createDependency(p.getRef()));
            }
            beans.put(def.getId(), bean);
        }
    }

    public Object getBean(String id) { return beans.get(id); }
}
```

读 XML → 反射创建 → 反射注入 → 存 Map → `getBean` 取出。**这就是 BeanFactory 的原型。**

**第三步：Spring 1.0 落地**

```java
public interface BeanFactory {
    Object getBean(String name) throws BeansException;
    <T> T getBean(String name, Class<T> requiredType) throws BeansException;
}
```

`XmlBeanFactory` 实现上述流程。"单例 Bean 工厂"成型：**一个按 name/type 查找已装配 Bean 的工厂，Bean 默认单例**。

### 3. 为什么默认单例

- 大部分业务 Service（`OrderService`/`UserService`）**无状态**，多实例纯浪费；
- 装配一次反复用，启动快、内存省；
- 框架只需维护一份依赖图，简单。

这不是 Spring 专利：EJB 无状态会话 Bean 也是容器池化复用的单例语义，CDI 的 `@ApplicationScoped` 也是单例——**社区共识**。

***

## 七、DI 一定要单例么：scope 是独立维度

### 1. 规范层答案：不强制

- **JSR 330** 只定义注入注解，**不规定 scope**；
- **CDI** 默认 `@Dependent`（每次注入新建），单例要显式 `@ApplicationScoped`；
- **Spring** 默认 singleton，但提供 prototype/request/session/application；
- **Guice** 默认 prototype，单例要显式 `@Singleton`。

| 容器 | 默认 scope | 显式单例 |
|---|---|---|
| Spring | **singleton** | `@Component`（默认即是） |
| CDI | `@Dependent` | `@ApplicationScoped` |
| Guice | prototype | `@Singleton` |

### 2. 概念层答案：DI 与单例是两个正交维度

DI 做四件事——创建、装配、生命周期管理、查找。**这四件事都和"是否单例"无关**：容器可以每次 new 再装配，也可以缓存复用。

- **DI 是装配问题**；
- **scope 是复用策略**。

### 3. Spring 提供的 scope

| scope | 含义 | 典型用法 |
|---|---|---|
| singleton（默认） | 容器内一份 | 无状态业务 Service |
| prototype | 每次获取都新建 | 有状态短生命周期对象 |
| request | 每 HTTP 请求一份 | Web 请求级状态 |
| session | 每 HTTP Session 一份 | 购物车、用户偏好 |
| application | 每 ServletContext 一份 | 应用级共享缓存 |

### 4. 什么时候不能用单例

```java
// ❌ 反例：有状态 Bean 用 singleton 会数据串
@Service
public class ShoppingCart {
    private final List<Item> items = new ArrayList<>();
    public void add(Item i) { items.add(i); }
}

// ✅ 正确：有状态 → session 或 prototype
@Component
@SessionScope
public class ShoppingCart {
    private final List<Item> items = new ArrayList<>();
}
```

**判据**：Bean 是否持有可变实例状态。无状态用 singleton，有状态必须改 scope。

***

## 八、Spring singleton 与 GoF Singleton 的本质差异

这是全文最容易被字面意思掩盖的一个关键点：两者都叫"singleton"，工程语义完全不同。

### 1. GoF Singleton：单例性靠类自己

```java
public class GoFConfig {
    private static GoFConfig INSTANCE;       // 静态字段持有
    private GoFConfig() { loadConfig(); }    // 私有构造，外部 new 不了
    public static GoFConfig getInstance() {
        if (INSTANCE == null) INSTANCE = new GoFConfig();
        return INSTANCE;
    }
}
```

- 唯一性靠 **`private` 构造 + `static` 字段**；
- 范围 = **每个 ClassLoader 一份**（Class 对象在 ClassLoader 内唯一，静态字段挂在 Class 上）；
- 类无法被正常 new，无法换实现，无法被继承替换。

### 2. Spring singleton：单例性靠容器 Map

```java
public class DefaultSingletonBeanRegistry {
    private final Map<String, Object> singletonObjects = new ConcurrentHashMap<>(256);

    protected Object getSingleton(String beanName) {
        Object o = singletonObjects.get(beanName);
        if (o == null) {
            o = createBean(beanName);              // 反射 new，不要求私有构造
            singletonObjects.put(beanName, o);     // 存进容器自己的 Map
        }
        return o;
    }
}
```

- 唯一性靠 **容器的 Map 缓存**；
- 范围 = **每个 ApplicationContext 一份**；
- 业务类构造可以是 public，类可以被正常 new，容器只是缓存了自己的那一份。

### 3. 代码证明：同一个类在两个容器里是两份

```java
var ctx1 = new AnnotationConfigApplicationContext();
var ctx2 = new AnnotationConfigApplicationContext();
ctx1.registerBean(OrderService.class, OrderService::new);
ctx2.registerBean(OrderService.class, OrderService::new);
ctx1.refresh();
ctx2.refresh();

OrderService a = ctx1.getBean(OrderService.class);
OrderService b = ctx1.getBean(OrderService.class);
OrderService c = ctx2.getBean(OrderService.class);

System.out.println(a == b);   // true  ← 同容器内一份
System.out.println(a == c);   // false ← 不同容器是两份
```

GoF 单例做不到这一点，因为 `static` 字段在 ClassLoader 内全局共享。

### 4. GoF 单例的三大工程灾难

**灾难 1：测试隔离破坏**

```java
@Test void testA() {
    GoFConfig cfg = GoFConfig.getInstance();
    cfg.setMockPayUrl("http://test");    // 改了"全局"
}
@Test void testB() {
    // cfg 仍残留 testA 改过的状态，测试顺序影响结果
}
```

静态字段是 JVM 全局状态，要重置只能靠反射暴力改。

**灾难 2：依赖无法替换**

```java
public class PaymentService {
    public void pay() {
        String url = GoFConfig.getInstance().getPayUrl();  // 主动拿，无法注入 mock
    }
}
```

类直接耦合到具体类，Test Double 进不来。

**灾难 3：多 ClassLoader 行为不可控**

每个 ClassLoader 都加载一份 Class，各自静态字段独立。Tomcat 每个 webapp 一个 ClassLoader，GoF 单例在这里语义破碎。

### 5. Spring 方案如何逐一化解

| 工程难题 | GoF 的困境 | Spring 的化解 |
|---|---|---|
| 测试隔离 | 静态全局污染 | 换 ApplicationContext 即新一份（`@DirtiesContext`、`@SpringBootTest`） |
| 依赖替换 | 直接耦合具体类 | 注入接口，mock 简单 |
| 配置外部化 | 创建参数硬编码 | 容器读 XML/yml 决定构造参数 |
| 生命周期销毁 | 静态字段 JVM 不死就在 | 容器 close 即销毁，资源可释放 |
| 多 ClassLoader | 范围不可控 | 单例范围明确绑容器 |

### 6. 对比总表

| 维度 | GoF Singleton | Spring singleton scope |
|---|---|---|
| 单例性来源 | 类的私有构造 + static 字段 | 容器的 Map 缓存 |
| 范围 | ClassLoader 内一份 | ApplicationContext 内一份 |
| 类能否正常 new | 不能 | 能（容器只是缓存自己那份） |
| 测试隔离 | 难 | 易（换容器即隔离） |
| 可替换性 | 差 | 好 |
| 反 singleton-anti-pattern | 违反（全局变量伪装） | 不违反（容器托管） |

### 7. 一个反直觉推论：scope 与线程安全正交

"Spring singleton 是否线程安全"这个问法本身有误——**线程安全取决于 Bean 是否无状态，与 scope 无关**：

| 场景 | 结论 |
|---|---|
| singleton + 无状态 Service | 天然线程安全，放心用 |
| singleton + 有状态字段 | 多线程读写冲突，必须改 scope 或加锁 |
| 多 ApplicationContext（测试） | 每容器一份，互不干扰 |

### 8. 核心思想跳跃

> Spring 把单例性从**"类的设计问题"**（私有构造 + 静态自管）挪到了**"容器的管理问题"**（Map 缓存 + 容器生命周期）。
>
> 容器销毁则实例销毁，容器重建则实例新建，不同容器互不可见。测试、替换、配置、销毁由此全部解放。

***

## 九、认知链总收束

四组问题最终收敛为一条链：

```
Tomcat 是 Java 程序
   → 容器（无论 Servlet 容器还是 IoC 容器）都是跑在 JVM 上的普通字节码
        ↓
IoC 不是突兀发明
   → 1988 思想原型 → 2003 Spring 框架化 → 2009 标准化 → 2010 EE 自己吸收
        ↓
Spring 替代的是 EJB 的工艺
   → POJO + 注解 + 反射 + 动态代理  替代  框架接口 + XML + 容器绑架
        ↓
POJO/Bean 工厂/单例是三个正交概念
   → POJO 决定"业务类是否被框架绑架"
   → Bean 工厂决定"对象怎么被装配"
   → scope 决定"装配后的复用策略"
        ↓
Spring singleton 不是 GoF singleton
   → 单例性从类的 static 字段转移到容器的 Map
   → 测试、替换、配置、销毁由此全部由容器接管
```

**最深的一层**：Spring 整个 IoC 设计可以归结为一次**责任转移**——

| 责任 | EJB/GoF 时代在谁身上 | Spring 时代在谁身上 |
|---|---|---|
| 对象创建 | 业务类（`new`/Home 接口） | 容器（反射） |
| 依赖装配 | 业务类（JNDI lookup） | 容器（`Field.set`） |
| 横切织入 | 框架接口绑架（`implements SessionBean`） | 容器（动态代理 + 注解） |
| 单例管理 | 业务类（`static` 自管） | 容器（Map 缓存） |
| 生命周期 | 业务类（被迫写 5 个 ejb 钩子） | 容器（`@PostConstruct`/`@PreDestroy` 可选回调） |

业务类由此回归 POJO——**不继承、不实现、不持有框架状态、不主动查找依赖**，只声明业务本身。框架从"身份绑架者"变成"装配服务者"。这就是 Spring 相对 EJB 最值钱的一次范式跳跃，也是 CDI 在 2010 年全面模仿这套范式的根本原因。

***

## 十、权威锚点

**S 级：一手规范与源头文档**

- JSR 330 Dependency Injection for Java：https://jcp.org/en/jsr/detail?id=330 —— DI 注解标准（`@Inject`/`@Named`/`@Provider`/`@Qualifier`），Spring 与 Google 联合提交。
- Jakarta CDI 规范：https://jakarta.ee/specifications/cdi/ —— EE 自己的 DI 容器规范，scope 模型（`@ApplicationScoped`/`@RequestScoped`/`@Dependent`）的权威定义。
- Spring Framework 官方文档（The IoC Container / Bean Scopes / AOP 章节）：https://docs.spring.io/spring-framework/reference/ —— singleton/prototype/request/session 等 scope 与容器 Map 机制的一手说明。
- Apache Tomcat 文档（Class Loading / Embedded 章节）：https://tomcat.apache.org/ —— Tomcat 多 ClassLoader 分层与嵌入式启动的一手说明。

**A 级：经典书与论文**

- Martin Fowler，*Inversion of Control Containers and the Dependency Injection pattern*（2004）：https://martinfowler.com/articles/injection.html —— IoC/DI 术语定型的源头文章。
- Rod Johnson，*Expert One-on-One J2EE Design and Development*（2002）—— Spring 设计动机与对 GoF 单例过度使用的批评出处。
- Erich Gamma 等，《设计模式：可复用面向对象软件的基础》（1994）—— GoF Singleton 与工厂模式的原始定义。
- Craig Walls，《Spring 实战》（Spring in Action）—— Spring 编程模型标准入门。
- 周志明，《深入理解Java虚拟机》—— ClassLoader、类加载与"单例范围"关系的中文系统讲解；《凤凰架构》—— EE 到 Spring Boot/云原生演进梳理。

**B 级：进一步延伸**

- JLS（Java Language Specification）第 8 章（类）与第 12 章（类加载、链接、初始化）—— `static` 字段与 Class 对象生命周期的规范层根。
- JVMS 第 5 章（Loading, Linking, and Initializing）—— ClassLoader 与 Class 对象唯一性的规范层根。
- Joshua Bloch，《Effective Java》第 3 条"用私有构造器或者枚举类型强化 Singleton 属性"与"single-element enum 单例"—— 对 GoF 单例现代写法的权威讨论。
