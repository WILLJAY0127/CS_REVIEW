# Q1 源码阅读手册：跟着一个 Bean 走完五步流水线

> 定位：主文告诉你"Bean 生命周期分五步"，本文带你**用调试器亲眼看到这五步**。读十遍源码解析，不如自己跟一遍断点。
> 配套：[Q1_Bean生命周期与BeanPostProcessor.md](Q1_Bean生命周期与BeanPostProcessor.md)（主答案）｜ [Q1_学习路径_从死循环到三级缓存.md](Q1_学习路径_从死循环到三级缓存.md) ｜ [Q1_补充_高频注解与机制的坑点.md](Q1_补充_高频注解与机制的坑点.md)

---

## 一、环境：十分钟搭好调试现场

### 依赖：只要 spring-context

不要 Spring Boot —— Boot 启动会额外造几百个 Bean，断点会停到你怀疑人生。纯净版才能看清主线：

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>6.1.14</version>
</dependency>
```

然后在 IDEA 里对依赖 **Download Sources**（Maven 面板右上角图标，或点进任意 Spring 类后顶部出现的提示条）。不下载源码，跟进去看到的是反编译残影，行号对不上、变量名是 `var1` 这种，体验极差。

### 最小 demo：一个能触发三级缓存的环

```java
package com.example.demo;

@Component
public class A {
    @Autowired
    B b;
}

@Component
public class B {
    @Autowired
    A a;
}

public class Main {
    public static void main(String[] args) {
        var ctx = new AnnotationConfigApplicationContext("com.example.demo");
        A a = ctx.getBean(A.class);
        System.out.println(a.b.a == a);   // true：环上所有人拿到的是同一个 A
    }
}
```

注意一个版本差异：**纯 spring-context 默认允许字段/setter 注入的循环依赖**，Spring Boot 2.6+ 才默认禁止。这个 demo 用纯 spring-context 正好能跑起来，可以看到三级缓存救场的全过程。

---

## 二、怎么进 doCreateBean：两条路线

你之前说"第一行我都找不到"——因为 `doCreateBean` 没有任何地方写着"入口在此"，它是被 `refresh()` 层层调进去的。给你两条路线：

### 路线 A：断点带路（强烈推荐，先建立体感）

思路：**不在源码里找入口，让程序自己停在入口处。**

1. 在 `A` 的构造器里打一个断点（哪怕构造器是空的，打在类里任意可执行行上）；
2. Debug 启动 `Main`；
3. 程序停住时，看 IDEA 左侧的 **Frames（调用栈）面板，从下往上读** —— 这就是"谁把我造出来的"完整链路：

```text
A.<init>                                              ← 你在这
createBeanInstance        AbstractAutowireCapableBeanFactory
doCreateBean              AbstractAutowireCapableBeanFactory   ← 目标！
createBean                AbstractAutowireCapableBeanFactory
doGetBean                 AbstractAutowireCapableBeanFactory
getBean                   ...
preInstantiateSingletons  DefaultListableBeanFactory
finishBeanFactoryInitialization   AbstractApplicationContext
refresh                   AbstractApplicationContext
AnnotationConfigApplicationContext.<init>
main                      Main
```

4. 在 Frames 面板里**点击 `doCreateBean` 那一帧**，编辑器直接跳到对应源码行 —— 这就是入口，根本不用自己找。顺手在这一行补个断点，下次直接停。

### 路线 B：主动找上门（验证用）

1. `Ctrl + N`（类搜索）输入 `AbstractAutowireCapableBeanFactory`；
2. 如果打开的是 `.class` 且行号诡异，先点顶部 **Download Sources**；
3. `Ctrl + F12`（文件结构）输入 `doCreateBean` 回车定位；
4. **认准带 `do` 的那个**：`createBean` 是外壳（做准备工作），`doCreateBean` 才是真正干活的。Spring 源码大量 `xxx` / `doXxx` 成对出现，记住口诀：**找带 do 的**。

### "认脸"代码：确认你站对了地方

`doCreateBean` 开头长这样：

```java
protected Object doCreateBean(String beanName, RootBeanDefinition mbd, @Nullable Object[] args)
        throws BeanCreationException {
    // Instantiate the bean.
    BeanWrapper instanceWrapper = null;
    ...
    instanceWrapper = createBeanInstance(beanName, mbd, args);   // 流水线①：new 实例
```

看到 `BeanWrapper instanceWrapper` + `createBeanInstance(beanName, mbd, args)` 这两行，就说明站对了。

---

## 三、断点条件：`"a".equals(beanName) || "b".equals(beanName)` 是什么意思

### 为什么需要条件断点

容器启动时不只造你的 A 和 B，还要造几十个内部 Bean（各种处理器、事件广播器、配置解析器……）。断点裸打，会停几十次才轮到 A，直接崩溃。条件断点 = 只在造 A 或 B 时才停。

### 逐词拆解

```java
"a".equals(beanName) || "b".equals(beanName)
```

| 片段 | 含义 |
|---|---|
| `beanName` | 当前正在创建的这个 Bean 的名字 —— 就是 `doCreateBean` 的第一个参数。IDEA 的断点条件里**可以直接引用当前作用域的参数和局部变量** |
| `"a"` | Bean 的默认名字 = **类名首字母小写**：`A` → `"a"`，`OrderService` → `"orderService"` |
| `||` | Java 的"或"：是 a **或**是 b，都停 |
| 为什么写 `"a".equals(beanName)` 而不是 `beanName.equals("a")` | 老手防 NPE 的习惯：字符串常量放前面，即使 `beanName` 为 null 也不会抛空指针 |

整句翻译成人话：**"如果现在正在造的 Bean 叫 a，或者叫 b，就停下来；否则当没看见，继续跑。"**

### 在 IDEA 里怎么设置

1. 右键断点红点 → 弹出断点属性窗口；
2. 找到 `Condition` 输入框，粘贴 `"a".equals(beanName) || "b".equals(beanName)`；
3. 点 Done。红点右下角多一个小标记，表示这是条件断点。

注意：如果类上写了 `@Component("orderService")` 这种自定义名字，条件里的 `"a"` 要换成你自定义的名字。

---

## 四、断点清单：6 + 1 个位置

在 `AbstractAutowireCapableBeanFactory` 和 `DefaultSingletonBeanRegistry` 两个类里打：

| # | 位置 | 对应流水线步骤 | 停顿时看什么 |
|---|---|---|---|
| 1 | `doCreateBean` 第一行 | 开始造 Bean | 参数 `beanName` 是谁 |
| 2 | `createBeanInstance(...)` 返回处 | ① 实例化完成 | `beanInstance` 已存在，但**字段全是 null**（半成品出生证明） |
| 3 | `addSingletonFactory(beanName, ...)` | ①之后的兜底 | 三级缓存放进了一个 lambda（A 的"早期引用工厂"） |
| 4 | `populateBean(beanName, mbd, instanceWrapper)` | ② 属性填充 | 填充前后对比 `b` 字段：null → 有值 |
| 5 | `initializeBean` 里的 `applyBeanPostProcessorsAfterInitialization` | ③ 初始化/代理 | 返回值是否换了一个对象（换了 = 被代理了） |
| 6 | `DefaultSingletonBeanRegistry#addSingleton` | ④ 进一级缓存 | `singletonObjects` 多一个，二三级被清掉 |
| +1 | `getSingleton(String beanName, boolean allowEarlyReference)` | **观察点**（读懂即可，不一定要停） | 三级缓存的查询逻辑本体，环的解法全在这十几行里 |

---

## 五、观察重点：三个 map 的五步剧本

在 Debug 窗口的 **Watches**（监视）里加三个表达式，全程盯住：

```java
this.singletonObjects        // 一级缓存：成品
this.earlySingletonObjects   // 二级缓存：半成品的"提前暴露版"
this.singletonFactories      // 三级缓存：生产半成品的工厂（lambda）
```

（这三个 map 定义在 `DefaultSingletonBeanRegistry` 上；断点停在工厂类里时，在 Variables 里翻一下或直接加 Watch。）

按 F9 逐段放行，你会亲眼看到这个剧本：

1. **造 A**：断点 3 停住 → `singletonFactories` 里多了 `"a"` → 一个 lambda。
2. **填充 A**：`populateBean` 发现要注入 B → 内部调 `getBean("b")` → **调用栈套娃**：`doCreateBean("a")` 上面又叠了一个 `doCreateBean("b")`。
3. **造 B、填充 B**：B 也要 A → 走到 `getSingleton("a", true)` → **命中三级缓存**，执行 lambda 拿到 A 的半成品 → 放进**二级**，删掉三级。
4. **B 完工**：断点 6 停住 → `"b"` 进 `singletonObjects`。
5. **回到 A**：A 的 `populateBean` 继续（拿到的 B 已是成品）→ A 走完初始化 → `"a"` 进一级，二三级清场。

最后 `a.b.a == a` 打印 `true`：环上所有指针指向同一个 A。这就是三级缓存存在的全部理由。

---

## 六、两个对照实验：改一行，看懂设计边界

### 实验 1：换成构造器注入

```java
@Component
public class A {
    final B b;
    public A(B b) { this.b = b; }
}
```

（B 同理改成构造器要 A。）再跑：**断点 3 永远等不到** —— 程序在断点 2 `createBeanInstance` 就直接炸出 `BeanCurrentlyInCreationException`。

原因：构造器要 B 时 B 还不存在；转头造 B，B 又要 A，而 A 此刻**连半成品都不是**（连 `new` 都没完成），根本走不到 `addSingletonFactory`，三级缓存想救都没东西可救。

结论：三级缓存救的是"字段/setter 环"，救不了"构造器环"—— 而启动期就炸**反而是好事**：问题在启动时暴露，不留到运行期。

### 实验 2：去掉环（A 不再依赖 B）

断点 3 照常停住 —— 三级缓存对**每个单例都放**，不问有没有环。但全程没有任何人来取 `"a"` 的工厂；最后 `addSingleton` 时顺手把它清掉。

结论：三级缓存是**兜底保险**，无环时纯路过。看到它存在不等于有环，**被取走才说明有环**。

---

## 七、阅读纪律：别淹死在 refresh() 里

1. **只 step into（F7）这五个方法**：`createBeanInstance`、`addSingletonFactory`、`populateBean`、`initializeBean`、`getSingleton`。其余一律 step over（F8）飞过去。
2. `refresh()` 里 90% 的内容（环境准备、BeanFactoryPostProcessor、国际化、事件机制）跟本次目标无关，第一遍一律不展开。
3. 第一遍的产出物只有一样：**一张亲手画的调用栈图**：

```text
main
 └─ refresh
     └─ finishBeanFactoryInitialization
         └─ preInstantiateSingletons
             └─ doGetBean("a")
                 └─ doCreateBean("a")
                     ├─ createBeanInstance        ① new A（字段全 null）
                     ├─ addSingletonFactory("a")  兜底：A 的工厂进三级缓存
                     ├─ populateBean              ② 填 A.b
                     │   └─ getBean("b")          ── 套娃 ──
                     │       └─ doCreateBean("b")
                     │           ├─ createBeanInstance   new B
                     │           ├─ populateBean         填 B.a
                     │           │   └─ getSingleton("a")  ★ 命中三级缓存
                     │           │        A 半成品 → 放进二级，删三级
                     │           └─ initializeBean
                     │       └─ addSingleton("b")          B 进一级
                     ├─ initializeBean            ③ A 初始化（本例无代理）
                     └─ addSingleton("a")         ④ A 进一级，清二三级
```

> 一句话总结：**第一遍源码阅读的产出物不是"看懂了"，而一张调用栈图 + 三组 map 的截图。** 图能默画出来，Q1 主文的五步流水线就真正长在你身上了。
