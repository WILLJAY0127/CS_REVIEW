# JDK 早期版本史话（1.1 → 6）：Java 如何从浏览器玩具长成企业平台

> 本文按周志明《深入理解Java虚拟机》开篇的版本脉络，逐版拆解 JDK 1.1 / 1.3 / 1.4 / 5 / 6 的关键技术特性，回答三个问题：**每一版加了什么、为什么加、今天还活着么**。这五版共同塑造了今天你写的每一行 Java 代码，也是理解后续 Servlet/EJB/Spring/JUC 全套生态的历史前提。与同目录 Spring 系列文档配套：那几篇讲"对象怎么装、物怎么装"，本篇讲"Java 这套平台本身怎么长出来的"。

## 8+1 总览卡

1. **JDK 1.1（1997）植入企业基因**：JAR（打包分发）、JDBC（连数据库）、JavaBeans（组件规约）、RMI（跨 JVM 调用）——一年补齐分发/数据/组件/分布式四个企业基础维度。
2. **JDK 1.3（2000）给 J2EE 补底层**：JNDI 从扩展升级为平台服务（对象目录/配置外部化）、RMI-IIOP（RMI 协议跑在 CORBA IIOP 上以支持多语言互操作）、Timer API——直接服务 1999 年发布的 J2EE 1.2。
3. **JDK 1.4（2002）工程基础设施补齐**：正则表达式、异常链、NIO、日志类、XML 解析器、XSLT——让标准 JDK"开箱即用"，不依赖第三方库就能做企业开发。
4. **JDK 5（2004）历史拐点**：语法六件套（自动装箱/泛型/枚举/注解/可变参数/foreach）+ JMM 重写（JSR 133，happens-before）+ `java.util.concurrent`（JSR 166，Doug Lea 主导）——Java 从"半成品语言"进入"现代语言"。
5. **JDK 6（2006）外部保守、内部激进**：API 只加 Rhino/注解处理器/HttpServer 三件小事，但 JVM 内部做了锁升级（偏向→轻量→重量）、CMS GC 转正、ServiceLoader 标准化、CDS 类数据共享。
6. **一条存活率规律**：JDK 加的工程库分两类——成为"基础设施"的统治至今（JAR/JDBC/NIO/正则/异常链/泛型/注解/concurrent/ServiceLoader）；被更好的第三方库超越或随时代退场的边缘化（JavaBeans GUI 规约/RMI/RMI-IIOP/CMS/偏向锁/XSLT/JDK logging）。
7. **命名线索**：JDK 1.5 起品牌从"1.x"改为"Java 5"，宣告进入新阶段；J2EE 在 JDK 6 时代更名 Java EE，2017 年移交 Eclipse 后更名 Jakarta EE（包名 `javax.*` → `jakarta.*`）。
8. **与后续生态的接续点**：JDK 5 注解 → Spring 注解化 → Spring Boot 自动配置；JDK 6 注解处理器 → Lombok/MapStruct → Quarkus/Spring AOT 编译期装配；JDK 5 NIO → Netty → Tomcat NIO Connector / WebFlux；JDK 5 concurrent → 一切 Java 并发框架的根。

**一句话主线**：1.1 让 Java "能做企业开发"，1.2 切分平台，1.3 给 J2EE 补底层，1.4 让 JDK 自给自足，5 把语言和并发现代化，6 把 JVM 内部做扎实——这五版是 Java 平台的"奠基期"，之后所有框架（Spring/Netty/Tomcat/Hibernate）都是在这套地基上盖楼。

***

## 目录

1. [JDK 1.1（1997.2）：企业基因四件套](#一jdk-1119972企业基因四件套)
2. [JDK 1.3（2000.5）：给 J2EE 补底层](#二jdk-1320005给-j2ee-补底层)
3. [JDK 1.4（2002.2）：工程基础设施补齐](#三jdk-1420022工程基础设施补齐)
4. [JDK 5（2004.9）：语法大改 + JMM + 并发包](#四jdk-520049语法大改--jmm--并发包)
5. [JDK 6（2006.12）：外部保守，内部激进](#五jdk-6200612外部保守内部激进)
6. [五版脉络总览](#六五版脉络总览)
7. [特性存活率总表](#七特性存活率总表)
8. [权威锚点](#八权威锚点)

***

## 一、JDK 1.1（1997.2）：企业基因四件套

### 历史定位

JDK 1.0（1996.1）时代 Java 还只是"浏览器里跑 Applet 小动画的语言"，API 贫乏。JDK 1.1 一年之内补齐四件企业级能力，Java 的企业基因全部植入。1998 年 JDK 1.2 的 J2SE/J2EE/J2ME 三大平台分家，正是建立在 1.1 这套地基之上。

### 1. JAR 文件格式（Java Archive）

**是什么**：`.jar` 本质是 zip 压缩包 + `META-INF/MANIFEST.MF` 元数据清单，可装 `.class`、资源文件、签名信息。

**解决了什么**：JDK 1.0 没有统一打包格式，分发应用要散放几十个 `.class` 文件，网络传输慢、易篡改、版本管理难。JAR 带来打包聚合、压缩传输、元数据清单、数字签名、统一类加载五项能力。

典型 MANIFEST：

```
Manifest-Version: 1.0
Main-Class: com.x.Application
Class-Path: lib/utils.jar
Sealed: true
```

**后续影响**：JAR 是 Java 整套打包模型的原型——WAR = JAR + WEB-INF 结构；EAR = JAR + 多模块聚合；Spring Boot fat jar = JAR + BOOT-INF 嵌套结构。JAR 规范 1997 年定型，沿用至今未变。

### 2. JDBC（Java Database Connectivity）

**是什么**：Java 连接关系数据库的标准 API，定义 `Driver`/`Connection`/`Statement`/`ResultSet` 一组接口，让同一份 Java 代码可操作任何数据库。

```java
try (Connection conn = DriverManager.getConnection(url, user, pwd);
     PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?")) {
    ps.setInt(1, 100);
    try (ResultSet rs = ps.executeQuery()) {
        while (rs.next()) {
            System.out.println(rs.getString("name"));
        }
    }
}
```

**解决了什么**：JDK 1.0 只能靠 JDBC-ODBC 桥接 C 风格的 ODBC API，跨平台差、性能差、厂商各自扩展。JDBC 用"接口-实现分离"范式统一：

```
java.sql.*（接口，在 JDK 里）
      ↑ uses
应用代码（只面向接口）
      ↑ implements
各厂商 Driver（com.mysql.cj.jdbc.Driver / oracle... / postgresql...）
```

**工程意义**：这是 Java 生态最经典的"规范定接口、厂商写实现"范式的起源——后来的 JPA(Hibernate)、JTA(Atomikos)、Servlet(Tomcat)、JMS(ActiveMQ) 全部照搬这套模式。

**后续影响**：Spring JDBC、MyBatis、Hibernate 全部建立在 JDBC 之上；连接池 HikariCP 是工程增强；JPA 底层仍是 JDBC。**今天所有 ORM 的最底层跑的还是 1997 年这套 API。**

### 3. JavaBeans

**是什么**：Java 组件规约，给类定一套"可被工具识别"的约定，最初服务 IDE 拖拽式可视化开发。

三条核心约定：

```java
public class User implements Serializable {
    private String name;
    private int age;

    public User() { }                                    // 1. 无参构造（反射创建）

    public String getName() { return name; }             // 2. getter/setter 命名约定
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
}
```

**三层演进（最易混淆的点）**：

| 阶段 | 名字 | 用途 |
|---|---|---|
| 1997 JDK 1.1 | **JavaBeans**（原始） | GUI 组件规约，服务 IDE 拖拽 |
| 1999 J2EE 1.2 | **Enterprise JavaBeans（EJB）** | 服务端组件规约，带事务/安全/远程调用 |
| 2003+ | **POJO + getter/setter 的"JavaBean"** | 简单数据载体 |

今天说"User 是个 JavaBean"指第三层含义，与 1997 年 GUI 规约已无关，但命名约定和"Bean"术语统治整个 Java 生态——Spring 容器装配的对象就叫 Bean。

### 4. RMI（Remote Method Invocation）

**是什么**：Java 原生远程调用机制，让一个 JVM 里的对象像调本地方法一样调用另一个 JVM 里对象的方法。

工作模型：客户端持有 Stub（代理）→ 序列化 + 网络 → 服务端 Skeleton → 反射调用真实对象；服务端用 `rmiregistry`（端口 1099）注册服务。

```java
public interface UserService extends Remote {
    User find(int id) throws RemoteException;
}

// 服务端注册
LocateRegistry.createRegistry(1099);
Naming.rebind("UserService", new UserServiceImpl());

// 客户端调用
UserService svc = (UserService) Naming.lookup("rmi://localhost:1099/UserService");
User u = svc.find(100);   // 像本地调用
```

**解决了什么**：1997 年分布式主流是 CORBA（C++ 主导，IDL+ORB，重）和 DCOM（微软）。RMI 给了纯 Java 写法：Java 接口定义契约、Java 序列化传输、调用风格像本地方法。

**后续影响**：EJB 远程调用和 JNDI 查找底层都基于 RMI；Stub/Skeleton 的"远程代理 + 反射调用"模式被 Dubbo/gRPC Java/Spring HttpInvoker 继承。RMI 协议本身在微服务时代退场（被 JSON/gRPC 取代），**但 JDK 内部的 JMX 远程管理至今仍用 RMI**。

### 四件套的内在联系

| 技术 | 解决的维度 |
|---|---|
| JAR | **分发**——代码怎么打包传输 |
| JDBC | **数据**——怎么连关系数据库 |
| JavaBeans | **组件**——类怎么被工具识别 |
| RMI | **分布式**——怎么跨 JVM 调用 |

四个加起来刚好覆盖企业级开发全部基础维度，这是 Sun 1997 年让 Java 进企业的判断。

***

## 二、JDK 1.3（2000.5）：给 J2EE 补底层

### 历史定位

JDK 1.2（1998.12）切分 J2SE/J2EE/J2ME 三大平台后，JDK 1.3 负责给 J2EE 补分布式基础设施，是 J2EE 1.2（1999）真正能大规模落地的版本基础。本版无语法改动，全在类库和协议层。

### 1. Timer API（`java.util.Timer`）

Java 第一次内置定时任务能力：

```java
Timer timer = new Timer();
timer.schedule(new TimerTask() {
    public void run() { System.out.println("每 1 秒一次"); }
}, 0, 1000);
```

之前要自己 `new Thread` + `sleep` 循环或依赖 OS 的 cron。Timer 内部单线程 + 最小堆任务队列，但有两个固有缺陷：**单线程**（一个任务卡死拖垮全部）、**未捕获异常会终止整个 Timer 线程**。

JDK 5 因此引入 `ScheduledThreadPoolExecutor`（线程池 + 异常隔离）替代；再往后 Spring `@Scheduled`、Quartz、XXL-Job 都建立在更完善的调度框架上。**起点是 JDK 1.3 的 Timer。**

同期还有 `BigDecimal`/`BigInteger` 方法完善、`StrictMath`（保证跨平台浮点结果严格一致）等数学运算补齐。

### 2. JNDI 从扩展服务升级为平台级服务

**JNDI（Java Naming and Directory Interface）** 是一组"按名字查找对象"的标准 API，本质是对象目录服务：

```java
Context ctx = new InitialContext();
ctx.bind("java:comp/env/jdbc/mydb", dataSource);
DataSource ds = (DataSource) ctx.lookup("java:comp/env/jdbc/mydb");
```

JDK 1.1 时代 JNDI 是独立扩展包（要单独下 `jndi.jar`），JDK 1.3 把 `javax.naming.*` 并入标准库，开箱即用。

**为什么对 J2EE 极关键**：J2EE 整套部署模型建立在 JNDI 之上——找 DataSource、JMS 连接工厂、EJB、环境变量、Mail Session 全部 `lookup`。EJB 2.x 的"配置外部化"完全靠它：应用服务器启动时按 web.xml/ejb-jar.xml 把资源注册进 JNDI 树，应用代码不直接 new，从而不改代码就能切换开发/测试/生产环境。

**设计本质**：JNDI 是 Service Locator 模式的标准实现（主动查找），与 DI（被动注入）是两种对立的解耦方式。Spring IoC 兴起后 JNDI 在业务代码中萎缩，Tomcat/WildFly 仍保留 JNDI 配置 DataSource 的能力，Spring Boot 推荐用 application.yml 替代。

**安全警示**：2016 年起 Jackson/Fastjson 反序列化漏洞、2021 年 Log4j2 漏洞（Log4Shell）都利用 JNDI lookup 经 RMI/LDAP 恶意加载远程类，JNDI 在反序列化场景从此被视为高危面。

### 3. RMI-IIOP：RMI 协议跑在 CORBA IIOP 上

**背景**：JDK 1.1 的 RMI 用私有协议 JRMP，只能 Java↔Java。而 1997 年企业级分布式主流是跨语言的 CORBA（IDL 定义接口 + IIOP 传输）。

**JDK 1.3 的折中**：让 RMI 编程模型不变，但底层协议可切换为 IIOP，Java 序列化对象翻译成 IIOP 的 CDR 格式。这样 Java 写的 EJB 既能被 Java 客户端用 RMI 调，也能被 C++ 等 CORBA 客户端调。

**命运**：这是一次失败的押注。CORBA 在微服务时代被 REST/JSON、再被 gRPC/Protobuf 整体取代；RMI-IIOP 随 CORBA 一起退场——JDK 11 标记 deprecated，**JDK 15（JEP 385）直接从 JDK 移除 CORBA 模块**。

### 本版串讲

Timer/数学服务通用场景；**JNDI 平台化 + RMI-IIOP 两项直接服务 J2EE**。JDK 1.3 是"J2EE 的基础设施补丁版"，2000~2005 年大量企业项目跑的就是 JDK 1.3 + J2EE 1.2/1.3 组合。

***

## 三、JDK 1.4（2002.2）：工程基础设施补齐

### 历史定位

本版把企业开发要用的工具库全部从第三方收编进 JDK（正则原本靠 Jakarta ORO、日志靠 log4j、XML 靠 Xerces），让标准 Java 平台开箱即用。这也是 Java 第一次以 JSR 流程开发的版本。

### 1. 正则表达式（`java.util.regex`）

```java
Pattern p = Pattern.compile("(\\d{4})-(\\d{2})-(\\d{2})");
Matcher m = p.matcher("2026-10-09");
if (m.matches()) {
    System.out.println(m.group(1));   // 2026
}
```

`Pattern`（编译后正则，线程安全可复用）+ `Matcher`（一次匹配状态机）+ String 的 `matches`/`replaceAll`/`split` 便捷方法。Jakarta ORO/RegExp 全部退场。**今天几乎没有 Java 项目不碰正则，是 1.4 使用频率最高的特性之一。**

### 2. 异常链（Chained Exceptions）

`Throwable` 新增 `cause` 字段、`getCause()`/`initCause()` 和带 cause 的构造方法：

```java
try {
    // ...
} catch (SQLException e) {
    throw new MyBusinessException("操作失败", e);   // 原始异常作为 cause 保留
}
```

打印堆栈时递归输出 `Caused by: ...`，跨层包装也不丢根因。这是 1.4 里"最小但最重要"的特性——解决了企业开发最致命的调试痛点：异常堆栈断层。Spring 的 `DataAccessException` 体系等所有现代异常体系都建立在此之上。

### 3. NIO（New I/O）——本版最大技术进步

旧 `java.io` 三个痛点：**阻塞 I/O**（一个连接一个线程）、**数据多次复制**、**字节流/字符流模型不统一**。

NIO 三大核心：

- **Channel**：双向、可阻塞可非阻塞（`FileChannel`/`SocketChannel`/`ServerSocketChannel`）；
- **Buffer**：数据容器，position/limit/capacity 三指针 + `flip()` 切换读写模式；
- **Selector**：事件多路复用，一个线程监听几千个 Socket（Linux 底层 epoll、macOS kqueue、Windows IOCP）。

```java
Selector selector = Selector.open();
ServerSocketChannel ssc = ServerSocketChannel.open();
ssc.configureBlocking(false);
ssc.register(selector, SelectionKey.OP_ACCEPT);
while (true) {
    selector.select();
    for (SelectionKey key : selector.selectedKeys()) {
        if (key.isAcceptable()) { /* 新连接 */ }
        if (key.isReadable())   { /* 可读 */ }
    }
}
```

另有 `FileChannel.transferTo()` 基于 `sendfile` 实现零拷贝。

**后续影响**：JDK 7 NIO.2（`java.nio.file`、异步 Channel）；Netty 基于 NIO 封装；Mina/Vert.x/Undertow、Tomcat 8+ 默认 NIO Connector、Spring WebFlux 的 Reactor——**今天所有高性能 Java 网络框架的根都是 1.4 的 NIO**。

### 4. 日志类（`java.util.logging`，JSR 47）

内置 `Logger`/`Level`/`Handler`/`Formatter`，配置文件 `logging.properties`，按名字组成父子 Logger 树。

但因性能（早期同步、无异步 Appender）、配置灵活性、输出格式均不如 log4j/logback，JUL 没成为业务主流。**它的深远影响是催生了日志门面**：Commons Logging → SLF4J（编译时绑定）→ Logback/Log4j2。今天 Spring Boot 默认 logback + SLF4J，业务代码面向门面编程，底层实现可换。Tomcat 内部的 JULI 则是 JUL 的多 webapp 适配版。

### 5. XML 解析器（JAXP）

并入标准 API，提供两套模型：
- **DOM**：整棵 XML 读进内存建树，适合小文件随机访问（`DocumentBuilder`）；
- **SAX**：事件驱动、流式解析，适合大文件顺序处理，内存极小（`DefaultHandler` 回调）。

默认实现是 Sun 捐给 Apache 的 Xerces。2010 年后 JSON 崛起，XML 数据交换场景萎缩（Spring Boot 用注解 + yml），但 JAXP 仍活在 SOAP、SVG、Office 文档等场景，其"接口-实现分离"模式被 Jackson 继承。

### 6. XSLT 转换器（`javax.xml.transform`）

用 XML 写转换规则，把一份 XML 转成另一份 XML/HTML/文本，当年用于报表生成、企业集成消息转换、Cocoon 视图。JSON 与现代模板引擎（Thymeleaf/Freemarker）兴起后基本退场，仅银行/政府存量系统残留。**是 1.4 六特性里今天用得最少的一个。**

### 六特性的分化规律

- **成为基础设施、统治至今**：正则、异常链、NIO；
- **被更好的第三方库超越而边缘化**：JUL 日志、JAXP（JSON 主流后减少）、XSLT。

这揭示一个规律：**JDK 收编的工程库，要么成为基础设施，要么被更好的第三方库取代。**

***

## 四、JDK 5（2004.9）：语法大改 + JMM + 并发包

### 历史定位

Java 历史最大拐点。注意版本号从"1.5"品牌化为"Java 5"，"1.x"时代结束。本版把 Java 从"半成品企业语言"推进到"现代语言"：语法六件套 + JMM 重写（JSR 133）+ 并发包（JSR 166，Doug Lea 主导）同时落地。

### （一）语法六件套

#### 1. 自动装箱/拆箱

编译器在基本类型与包装类之间自动插入 `valueOf`/`intValue`，集合操作不再手写样板：

```java
List<Integer> list = new ArrayList<>();
list.add(42);          // 自动装箱
int n = list.get(0);   // 自动拆箱
```

三个高频陷阱：
- **Integer 缓存**：`valueOf` 缓存 `[-128,127]`，故 `Integer a=127,b=127; a==b` 为 true，`200` 则为 false——比较包装类永远用 `equals`；
- **拆箱 NPE**：对 `null` 包装类拆箱抛 NPE；
- **性能陷阱**：循环里对 `Long sum` 做 `+=` 会每次新建 Long 对象，应改用基本类型 `long`。

#### 2. 泛型（Generics）

集合获得编译期类型约束，消灭大量 ClassCastException：

```java
List<String> list = new ArrayList<>();
list.add(42);   // 编译期报错
String s = list.get(0);
```

**核心设计：类型擦除（Type Erasure）**。编译后 `<String>` 被擦除，JVM 只看到原始类型 `List`。代价：不能 `new T()`、不能 `new T[]`、不能用基本类型作类型参数（只能 `List<Integer>`）、运行时拿不到类型参数、某些重载冲突。

选擦除而非 C# 式具现化（reified）的原因是**向后兼容**——2004 年已有海量 1.4 代码，擦除让 `List<String>` 与裸 `List` 运行时是同一个类。代价由 Project Valhalla（专门化泛型，让 `List<int>` 合法）长期弥补，至今未完全落地。通配符 PECS 原则（`? extends` 生产者、`? super` 消费者）和桥接方法是进阶考点。

#### 3. 枚举（Enum）

替代 int 常量模式和手写"类型安全枚举"：

```java
public enum Color { RED, GREEN, BLUE }
```

**Java 枚举不是 C 那种 int 别名，而是语法糖**——本质是 `final class Color extends Enum<Color>`，每个常量是该类的一个 `public static final` 唯一实例。由此天然获得：单例保证、可有字段/构造器/抽象方法（常量相关方法体）、`Comparable`、序列化安全（`readResolve` 返回缓存）、可用于 switch；`EnumMap`/`EnumSet` 基于位数组，性能远超 HashMap。

```java
public enum Operation {
    PLUS("+")  { public double apply(double a, double b){ return a+b; } },
    MINUS("-") { public double apply(double a, double b){ return a-b; } };
    private final String symbol;
    Operation(String s){ this.symbol = s; }
    public abstract double apply(double a, double b);
}
```

《Effective Java》推荐用单元素枚举实现单例（线程安全 + 序列化安全）。**枚举是 JDK 5 设计最优雅的特性。**

#### 4. 动态注解（Annotations）

注解本质是实现 `java.lang.annotation.Annotation` 的特殊接口，分三种保留策略：`SOURCE`（编译丢弃，如 `@Override`）、`CLASS`（字节码保留、运行时不可见）、`RUNTIME`（可反射读取，框架注解全用它）。

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Service { String value() default ""; }
```

**这是 Spring 后续革命的根**：Spring 2.0（2006）`@Component`/`@Autowired` → 2.5 `@Controller`/`@RequestMapping` → 4 `@Configuration`/`@Bean` → Spring Boot `@SpringBootApplication` 自动配置；Jakarta CDI 也全面注解化。注解让配置从 XML 回到代码但保持元数据特性，是"约定优于配置"的前提。没有 JDK 5 注解就没有 Spring Boot。

#### 5. 可变长参数（Varargs）

```java
void log(String format, Object... args) { ... }
log("User %s is %d", "Alice", 30);
```

底层 `Object...` 编译为 `Object[]`，调用点自动打包。`String.format`/`printf`、`Arrays.asList(T...)`、JDK 9 `List.of` 都依赖它。与泛型结合时的堆污染警告由 JDK 7 的 `@SafeVarargs` 解决。

#### 6. 增强 for 循环（foreach）

```java
for (String s : list) { ... }
for (int n : arr)   { ... }
```

语法糖：数组翻译为索引循环，`Iterable<T>` 翻译为 `Iterator` 循环。为此 JDK 5 把 `Iterable` 引入 `java.lang`。JDK 8 后简单遍历仍用 foreach，链式处理转向 Stream。

### （二）JMM 重写（JSR 133）

JDK 1.4 之前的内存模型有严重缺陷：volatile 语义弱、`final` 字段可见性未定义、双重检查锁定（DCL）失效（`new Singleton()` 的"分配内存→调用构造器→赋值引用"可能重排序，其他线程看到"非 null 但未构造完"的对象）。

JDK 5 重写 JMM，引入 **happens-before** 规则体系：程序顺序、监视器锁（unlock → 后续 lock）、volatile（写 → 后续读）、线程启动（`start()` → 线程内操作）、线程终止（线程操作 → `join()` 返回）、传递性，以及 **final 字段规则**（final 字段写入 happens-before 对象引用对外可见）。

由此修复：
- **volatile 强化为轻量同步**，读写插入内存屏障；
- **final 字段语义明确**，不可变对象线程安全有了保障；
- **DCL 加 volatile 后安全**（StoreStore + StoreLoad 屏障阻止重排序）。

JSR 133 是 Java 并发的理论基石，C++11/C#/Go 的内存模型都借鉴了 happens-before。

### （三）`java.util.concurrent`（JSR 166）

JDK 1.4 时代并发只有裸 `synchronized`/`wait`/`notify`， Doug Lea 主导的 JUC 把并发"框架化"，四大板块：

| 板块 | 代表 | 作用 |
|---|---|---|
| 并发集合 | `ConcurrentHashMap`、`CopyOnWriteArrayList`、`ConcurrentLinkedQueue` | 分段锁/CAS 替代全局锁，读无锁写锁一段 |
| Executor 框架 | `ThreadPoolExecutor`、`Executors` | 任务与线程解耦，线程复用/队列/拒绝策略 |
| 同步工具 | `CountDownLatch`、`CyclicBarrier`、`Semaphore`、`ReentrantLock`、`ReadWriteLock`、`Condition` | 可中断/可超时/公平锁、读写分离、多条件队列 |
| 原子类 | `AtomicInteger` 等 `java.util.concurrent.atomic` | 基于 CPU CAS 的无锁原子操作 |

**JMM 与 JUC 同时落地不是巧合**：JMM 给理论契约（happens-before），JUC 给实践工具。后续 JDK 7 ForkJoinPool、JDK 8 CompletableFuture、JDK 9 Flow（响应式），以及 Tomcat 请求线程池、Spring `@Async`、Netty EventLoop、Akka/Reactor/RxJava 全部建立在 JUC 之上。

### 本版意义

1.4 之前四版解决"Java 能干什么"，JDK 5 重写"Java 怎么写"。这种一版塞进六件套 + JMM + JUC 的节奏在 Java 历史上空前绝后，是 Sun 主导的最后一版"激进 Java"。

***

## 五、JDK 6（2006.12）：外部保守，内部激进

### 历史定位

JDK 5 体量巨大，社区需要消化期。JDK 6 API 增量小，但 JVM 内部（锁、GC、类加载）做了大量优化，是 JDK 5 的消化期和 JDK 7/8 高性能的地基。

### （一）三个 API 改进

#### 1. 内置 Mozilla Rhino JavaScript 引擎

通过 `javax.script`（JSR 223）在 JVM 上运行 JS，是 Sun"JVM 支持多语言"战略的试探：

```java
ScriptEngine js = new ScriptEngineManager().getEngineByName("javascript");
js.eval("print('Hello from JS')");
```

路线演化：Rhino(6) → invokedynamic 字节码（JDK 7，JSR 292）→ Nashorn（JDK 8）→ JDK 9 弃用 → GraalVM Polyglot 接棒。Rhino 本身边缘化，今天残活于 JMeter JSR223 等脚本场景，但它是 JVM 多语言路线的起点。

#### 2. 编译期注解处理器（JSR 269）——本版最被低估的特性

JDK 5 注解只能运行时反射读；JDK 6 让工具在**编译期**扫描注解并生成新代码：

```java
@SupportedAnnotationTypes("com.x.MyAnnotation")
public class MyProcessor extends AbstractProcessor {
    public boolean process(Set<? extends TypeElement> annotations, RoundEnvironment env) {
        for (Element e : env.getElementsAnnotatedWith(MyAnnotation.class)) {
            // 用 Filer 生成新源码，下一轮编译
        }
        return true;
    }
}
```

与反射相比：编译期执行、零运行时开销、可生成新类、可调试。今天的 **Lombok**（`@Data` 编译期生成 getter/setter/equals/hashCode）、**MapStruct**（生成 DTO 转换代码）、**Dagger 2**（编译期 DI）、Hibernate 元模型、Spring Boot 配置元数据全部依赖它。更深远的是 **Quarkus/Micronaut/Spring 6 AOT 用编译期注解处理消除反射**，支撑毫秒级启动和 GraalVM Native Image。2006 年埋的种子，十年后成为 Java 编译期元编程的根。

#### 3. 微型 HTTP 服务器（`com.sun.net.httpserver`）

JDK 自带极简 HTTP/1.1 服务器，用于测试和原型：

```java
HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
server.createContext("/hello", exchange -> {
    String resp = "Hello";
    exchange.sendResponseHeaders(200, resp.length());
    exchange.getResponseBody().write(resp.getBytes());
});
server.start();
```

注意位于 `com.sun.*` 包、非标准 API、无 Servlet，生产不推荐。今天主要用于轻量测试/JDK 内部工具；主流选择仍是 Spring Boot 内嵌 Tomcat 或 Netty。

### （二）JVM 内部三大改进

#### 1. 锁与同步：synchronized 锁升级

JDK 6 之前 `synchronized` 每次都走 OS 互斥量（重量级锁），性能远逊于 JDK 5 的 `ReentrantLock`。JDK 6 引入按竞争程度自动升级的多级锁：

```
无锁 → 偏向锁 → 轻量级锁 → 重量级锁
```

- **偏向锁**：假设锁始终被同一线程持有，对象头 Mark Word 记录线程 ID，重入只需比对 ID，无 CAS，接近无锁；
- **轻量级锁**：出现竞争但不激烈时 CAS 自旋，避免阻塞；
- **重量级锁**：自旋失败后升级为 OS 互斥量 + monitor 队列。

优化后 90% 场景停留在偏向锁，`synchronized` 性能追平 `ReentrantLock`，"能用 synchronized 就别用 ReentrantLock"成为新共识。

注意：偏向锁的撤销需要 safepoint 全局暂停，在多核时代代价变大，**JDK 15（JEP 374）废弃偏向锁**——但它在 JDK 6~14 的 14 年里是并发性能关键。

#### 2. 垃圾收集：CMS 转正与并行 Old GC

- **CMS（Concurrent Mark Sweep）从实验性转产品级**：第一个主流低延迟 GC，流程为初始标记(STW) → 并发标记 → 重新标记(STW) → 并发清除，大部分工作与应用线程并发，把大堆 STW 从秒级压到几十毫秒；
- **Parallel Old GC**：老年代收集也多线程并行；
- 引入自适应调优（ergonomics）、大页内存支持。

CMS 的固有代价是 Mark-Sweep 不压缩导致**碎片**、以及**Concurrent Mode Failure**（并发速度跟不上分配时退化为长时间 Serial Old STW）。后续 G1（JDK 7 引入、9 成为默认）、ZGC（JDK 11 实验、后续 STW <1ms）接棒，**CMS 在 JDK 14（JEP 363）被移除**。JDK 6 把 CMS 转正是 Java GC 走向"低延迟"的起点。

#### 3. 类加载

- **多并行类加载**：类加载器可并行加载多个类（此前串行）；
- **ServiceLoader 标准化**：`META-INF/services/<接口全限定名>` 文件声明实现类，`ServiceLoader.load()` 自动发现。JDBC 4.0 起驱动靠它自动注册，不再需要 `Class.forName("com.mysql...")`。SLF4J 绑定、Spring Boot 自动装配的发现机制底层同源——这是"零配置"和 SPI 机制的根；
- **CDS（Class Data Sharing）**：核心类预处理成共享归档，多 JVM 实例共享，启动提速、内存下降。后续演化为 JDK 10 AppCDS、JDK 13 动态归档，理念终点是 GraalVM Native Image 的全量 AOT；
- 动态代理性能优化。

### 本版再评价

API 三件事里，Rhino 和 HttpServer 边缘化，**注解处理器成为长期资产**；内部改进里，偏向锁和 CMS 是服务了 14 年的"过渡性优化"（均已移除），**ServiceLoader 和 CDS 则是沿用至今的长期资产**。JDK 6 表面平静，实则埋下今天 Java 高性能与零配置的多条主线。

***

## 六、五版脉络总览

```
1997 JDK 1.1  植入企业基因
   JAR（分发）/ JDBC（数据）/ JavaBeans（组件）/ RMI（分布式）
        ↓ 让 Java "能做"企业开发
1998 JDK 1.2  切分三大平台（J2SE / J2EE / J2ME）+ Collections / Swing
        ↓
2000 JDK 1.3  给 J2EE 补底层
   JNDI 平台化（配置外部化/对象目录）/ RMI-IIOP（CORBA 互操作）/ Timer
        ↓ 让 J2EE 部署模型能跑起来
2002 JDK 1.4  工程基础设施补齐
   正则 / 异常链 / NIO / 日志 / JAXP / XSLT
        ↓ 让标准 JDK 开箱即用
2004 JDK 5   语法大改 + 并发 + JMM   ←─ 历史拐点
   装箱 / 泛型 / 枚举 / 注解 / varargs / foreach
   + JMM happens-before（JSR 133）
   + java.util.concurrent（JSR 166）
        ↓ 把"Java 怎么写"重写
2006 JDK 6   外部保守、内部激进
   Rhino / 注解处理器（JSR 269）/ HttpServer
   + 锁升级 / CMS 转正 / ServiceLoader / CDS
        ↓ 消化期 + 高性能地基
2011 JDK 7   invokedynamic / NIO.2 / try-with-resources / diamond
2014 JDK 8   Lambda / Stream / Optional / CompletableFuture
```

**一句话**：1.1~1.4 回答"Java 能干什么"（平台能力建设），5~6 回答"Java 怎么写、跑得多快"（语言与虚拟机现代化）。这五版是 Java 的奠基期，此后 Spring/Netty/Tomcat/Hibernate 等一切框架都在这套地基上盖楼。

***

## 七、特性存活率总表

| 版本 | 特性 | 2025 状态 |
|---|---|---|
| 1.1 | JAR | 存活，所有打包格式的基础 |
| 1.1 | JDBC | 存活，所有 ORM 的最底层 |
| 1.1 | JavaBeans（GUI 规约） | 规约消亡；getter/setter 约定与"Bean"术语统治生态 |
| 1.1 | RMI（JRMP） | 企业级退场，仅 JMX 等 JDK 内部使用 |
| 1.3 | Timer | 存活但不推荐，被 ScheduledThreadPoolExecutor 取代 |
| 1.3 | JNDI 平台化 | 业务代码退场，容器/JDK 内部仍在；反序列化高危面 |
| 1.3 | RMI-IIOP / CORBA | 死亡，JDK 15（JEP 385）移除 |
| 1.4 | 正则表达式 | 存活，日常必备 |
| 1.4 | 异常链（cause） | 存活，所有异常体系基础 |
| 1.4 | NIO | 存活，所有高性能网络框架的根 |
| 1.4 | java.util.logging | 边缘化，主流走 SLF4J + Logback/Log4j2 |
| 1.4 | JAXP（DOM/SAX） | 存活但使用减少，JSON 主流 |
| 1.4 | XSLT | 基本退场，存量系统残留 |
| 5 | 自动装箱 | 存活（注意缓存/NPE/性能三陷阱） |
| 5 | 泛型 | 存活（类型擦除的代价仍在，Valhalla 弥补中） |
| 5 | 枚举 | 存活，设计最优雅的特性之一 |
| 5 | 注解 | 存活，现代 Java 框架的根 |
| 5 | varargs / foreach | 存活 |
| 5 | JMM（JSR 133） | 存活，Java 并发理论基石 |
| 5 | java.util.concurrent | 存活，一切并发框架的根 |
| 6 | Rhino | 边缘化，被 Nashorn/GraalVM 取代 |
| 6 | 注解处理器（JSR 269） | 存活，Lombok/MapStruct/AOT 的根 |
| 6 | HttpServer | 边缘化，测试/内部工具用 |
| 6 | 偏向锁 | 死亡，JDK 15（JEP 374）废弃 |
| 6 | CMS GC | 死亡，JDK 14（JEP 363）移除，被 G1/ZGC 取代 |
| 6 | ServiceLoader（SPI） | 存活，零配置/自动发现机制的根 |
| 6 | CDS | 存活，演化为 AppCDS → Native Image 路线 |

***

## 八、权威锚点

**S 级：一手规范与文档**

- JDK 各版本发行说明（Oracle Java Archive / Release Notes）：https://www.oracle.com/java/technologies/java-archive.html —— 每版新增特性的官方清单。
- JSR 规范：
  - JSR 133 Java Memory Model：https://jcp.org/en/jsr/detail?id=133
  - JSR 166 Concurrency Utilities：https://jcp.org/en/jsr/detail?id=166
  - JSR 269 Pluggable Annotation Processing：https://jcp.org/en/jsr/detail?id=269
  - JSR 292 invokedynamic：https://jcp.org/en/jsr/detail?id=292
  - JSR 223 Scripting for the Java Platform：https://jcp.org/en/jsr/detail?id=223
- Java Language Specification / JVM Specification（现行版）：https://docs.oracle.com/javase/specs/ —— 泛型擦除、JMM happens-before、枚举编译形态的规范出处。
- 移除类 JEP：JEP 363（移除 CMS，JDK 14）、JEP 374（废弃偏向锁，JDK 15）、JEP 385（移除 RMI-IIOP/CORBA，JDK 15）：https://openjdk.org/jeps/

**A 级：经典书与一手文章**

- 周志明《深入理解Java虚拟机》——本文版本脉络的原始出处，锁升级/GC/JMM 演进的中文系统讲解。
- Brian Goetz 等《Java Concurrency in Practice》——JMM happens-before 与 JUC 的权威实战指南。
- Joshua Bloch《Effective Java》——枚举单例、泛型通配符（PECS）、包装类比较等最佳实践。
- Doug Lea，《Concurrent Programming in Java》及 JSR 166 相关材料——JUC 设计原始出处。
- Martin Fowler 等关于 POJO 命名（2000）与 DI（2004）的文章：https://martinfowler.com/

**B 级：延伸脉络**

- Oracle《The Java Tutorials》（JDBC、NIO、正则、并发、注解处理器各章）：https://docs.oracle.com/javase/tutorial/
- ServiceLoader SPI 机制与 JDBC 4.0 自动驱动加载：`java.util.ServiceLoader` Javadoc。
- GraalVM Native Image / Spring AOT 文档——注解处理器与 CDS 路线在云原生时代的终点形态。
