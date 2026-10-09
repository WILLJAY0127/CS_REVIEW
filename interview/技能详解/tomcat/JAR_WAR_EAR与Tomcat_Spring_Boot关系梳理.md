# JAR / WAR / EAR 与 Tomcat、Spring、Spring Boot 的关系：一次讲透打包与部署模型

> 本文解决一个高频混淆：EAR/WAR/JAR 分别是什么、Tomcat 到底是"服务器"还是"jar 依赖"、Spring 替 EE 干了什么、Spring Boot 凭什么一个 jar 就具备了完整 EE 能力。与同目录 [javaee.md](file:///d:/myfile/CS_REVIEW/interview/技能详解/tomcat/javaee.md)（Jakarta EE 规范是什么、怎么读 Servlet 规范）配套：那篇讲**契约层**，本篇讲**部署与装配的实物层**。

## 8+1 总览卡

1. **三种包打三种应用**：jar = 普通 Java 程序/类库；war = 一个 Web 应用（Servlet 容器的主食）；ear = 一个完整 Jakarta EE 企业应用（多模块，只有完整应用服务器能吃）。
2. **Tomcat 是"容器产品"不是"项目类型"**：它是 Jakarta Servlet 规范的实现软件，本职工作就是加载并运行 war；以 jar 形式出现时只是它的"嵌入式"用法。
3. **内外反转是关键模型**：传统模式 war 放进外置 Tomcat；Spring Boot 模式把 Tomcat 以 jar 形式塞进可执行 jar——**不是 Tomcat 提供 war 插槽，而是应用把容器装进肚子**。
4. **Spring 不碰底层 HTTP，但有自己的 Web 上层**：Socket/报文/Servlet 生命周期外包给 Tomcat；URL 路由、Controller、参数绑定由 Spring MVC 自己干。
5. **Spring 替代的是 EJB 这套编程模型，不是替代全部规范**：IoC/AOP/声明式事务/数据访问用 POJO + 注解重做；Servlet、JPA、Validation 等规范在 Spring 6 后直接以 `jakarta.*` 消费。
6. **EE 与 Spring Boot 能力对齐、方向相反**：EE 是"应用薄 + 容器厚（外置服务器，ear 部署）"；Spring Boot 是"应用厚 + 容器薄（库即能力，内嵌容器，可执行 jar 独立进程）"。
7. **EAR 基本随 EJB 退场**：新项目不再打 ear；war 在传统部署里仍常见；新业务的绝对主流是 Spring Boot 可执行 jar + 内嵌容器 + 容器镜像。
8. **学习上的结论**：学 Servlet 规范不亏——无论外置 Tomcat、Spring Boot 内嵌 Tomcat、Quarkus，只要走 Servlet 模型，底层契约是同一份。

**一句话**：打包格式的演进史（jar → war → ear → 可执行 jar）本质是"谁厚谁薄、谁装进谁"的装配反转史；理解了反转方向，Tomcat、Spring、Spring Boot 三者的关系就再也不会混。

***

## 目录

1. [三种打包格式：jar / war / ear](#一三种打包格式jar--war--ear)
2. [Tomcat 到底是什么：容器的两种形态](#二tomcat-到底是什么容器的两种形态)
3. [Spring 与 EE 的分工：替代了什么，保留了什么](#三spring-与-ee-的分工替代了什么保留了什么)
4. [Spring Boot 如何用一个 jar 对齐 EE 全部能力](#四spring-boot-如何用一个-jar-对齐-ee-全部能力)
5. [能力对照表](#五能力对照表)
6. [常见误解纠正（四个高频错误模型）](#六常见误解纠正四个高频错误模型)
7. [演进时间线](#七演进时间线)
8. [权威锚点](#八权威锚点)

***

## 一、三种打包格式：jar / war / ear

三者都是 zip 压缩包，区别只在**内部约定结构**和**谁来加载它**。

### 1. jar（Java Archive）

- 内容：`.class` 字节码 + 资源文件 + `META-INF/MANIFEST.MF`。
- 用途：类库（被别人依赖）或可执行 Java 程序（MANIFEST 里写 `Main-Class`，`java -jar app.jar` 启动）。
- 加载者：JVM 类加载器，不认识 Servlet、不认识 EJB。

### 2. war（Web Application Archive）

- 内容：Servlet、JSP、静态资源，外加约定目录：

```
myapp.war
├── WEB-INF/
│   ├── web.xml              ← Web 部署描述符（Servlet/Filter/Listener 注册，现代版本可纯注解）
│   ├── classes/             ← 你的 .class
│   └── lib/                 ← 本应用依赖的 jar
└── index.html、静态资源 ...
```

- 用途：一个完整的 **Web 应用**。
- 加载者：**Servlet 容器**（Tomcat/Jetty/Undertow）。丢进 Tomcat 的 `webapps/` 目录即自动解压部署。
- 注意：war 里**没有** HTTP 服务器本身——它假定外面有个容器负责监听端口、解析 HTTP、调用你的 Servlet。

### 3. ear（Enterprise Archive）

- 内容：多个模块 + 企业级部署描述符：

```
myapp.ear
├── META-INF/
│   └── application.xml      ← 声明内含哪些模块、安全角色、资源映射
├── myapp-web.war            ← Web 模块（可多个）
├── myapp-ejb.jar            ← EJB 模块（会话 Bean、消息驱动 Bean）
├── myapp-entities.jar       ← JPA 实体（常并入 ejb 模块）
└── lib/                     ← 跨模块共享类库
```

- 用途：一个**完整 Jakarta EE 企业应用**，一个事务可以横跨 Web → EJB → 多数据源/JMS。
- 加载者：**完整应用服务器**（WildFly、GlassFish、WebLogic、WebSphere）。Tomcat 不认 ear——它没有 EJB 容器、没有 JTA 事务管理器。

### 4. 一张表收尾

| 维度 | jar | war | ear |
|---|---|---|---|
| 是什么 | 类库/可执行程序 | 一个 Web 应用 | 一个完整企业应用（多模块） |
| 标志性文件 | MANIFEST.MF | WEB-INF/web.xml | META-INF/application.xml |
| 谁来运行 | JVM | Servlet 容器（Tomcat） | 完整应用服务器（WildFly 等） |
| 内含 HTTP 服务器 | 默认没有 | 没有（外置容器） | 没有（外置服务器） |
| 现状 | 绝对主流（Spring Boot 可执行 jar） | 传统部署仍常见 | 随 EJB 基本退场，仅存量系统 |

***

## 二、Tomcat 到底是什么：容器的两种形态

### 1. Tomcat 的身份：Servlet 规范的实现产品

Tomcat 不是一种"项目结构"，而是一个**用 Java 写的容器软件**，它实现了 Jakarta Servlet（以及 JSP、WebSocket）规范。规范要求的 `init()/service()/destroy()` 生命周期、Request/Response 对象、Filter 链、Session 管理，全部由 Tomcat 提供具体代码。

它有两种发行/使用形态：

### 2. 形态 A：独立容器（传统模式）

- 官方下载的是一个压缩包（`bin/` 启动脚本 + `lib/` 一堆 jar + `webapps/`）。
- 运维先启动 Tomcat 进程（它监听 8080），再把 war 放进 `webapps/`。
- 部署方向：**应用（war）→ 装进 → 外置容器（Tomcat）**。
- 应用自己不含服务器，多个 war 可共享同一个 Tomcat 进程。

```
              ┌──────────── Tomcat 进程 ────────────┐
HTTP :8080 →  │  app1.war   app2.war   app3.war     │
              └─────────────────────────────────────┘
```

### 3. 形态 B：嵌入式容器（Spring Boot 模式）

- Tomcat 官方同时发布 `tomcat-embed-core.jar`，它可以作为普通 Maven 依赖被任何 Java 应用引入。
- 应用启动时在 `main()` 方法里 new 一个 Tomcat 实例、注册 Servlet、启动——**服务器生命周期由你的应用代码控制**。
- 部署方向反转：**容器（jar）→ 被装进 → 应用（可执行 jar）**。

```
java -jar myapp.jar
   └── 一个 JVM 进程
        ├── 你的业务类
        ├── Spring MVC（DispatcherServlet）
        └── tomcat-embed-core.jar（内嵌 HTTP 监听）
```

### 4. Spring Boot 可执行 jar 的内部结构（理解反转的实物证据）

```
myapp.jar
├── org/springframework/boot/loader/     ← Spring Boot 自定义类加载器入口
├── BOOT-INF/
│   ├── classes/                         ← 你的业务代码
│   └── lib/
│       ├── tomcat-embed-core-10.x.jar   ← 整个 Tomcat 在这儿
│       ├── spring-web-6.x.jar
│       ├── spring-webmvc-6.x.jar
│       └── hibernate-core-7.x.jar ...
└── META-INF/MANIFEST.MF  (Main-Class 指向 JarLauncher)
```

这就是"一个 jar 具备 EE 能力"的物理真相：**它不是一个 jar，它是一个把容器和所有能力库一起打进去的自包含部署单元**。jar 内嵌 `tomcat-embed-core` 等价于传统架构里"应用 + 一台专用 Tomcat"，但进程模型是一个应用一个进程，天然契合容器化（Docker 一个镜像一个服务）。

***

## 三、Spring 与 EE 的分工：替代了什么，保留了什么

### 1. Spring 的起源：替代 EJB 的重型组件模型

EJB 2.x 时代（2000 年代初）写一个业务组件要写 Home 接口、组件接口、Bean 类、部署描述符，且必须打包到应用服务器。Rod Johnson 2002 年写《Expert One-on-One J2EE Design and Development》，用 POJO + 接口 + 轻量级容器给出替代方案，这就是 Spring 的起点。

Spring 核心只干两件事：
- **IoC/DI 容器**：对象的创建、装配、生命周期交给容器（`@Component`/`@Autowired`）；
- **AOP**：把事务、日志、安全这些横切逻辑织入普通方法。

在这两块基石上，声明式事务、数据访问、安全、Web MVC 等能力被逐个用 POJO + 注解重做——**能力对齐 EJB/EE，重量大幅下降**。

### 2. 但 Spring 不做底层 HTTP

Spring 始终没有自己写 HTTP 服务器和 Servlet 引擎，而是定义对 Servlet 容器的适配层，默认外包给 Tomcat（可换 Jetty/Undertow）。分工切在 Servlet 这一层：

| 层次 | 职责 | 承担者 |
|---|---|---|
| 连接层 | TCP 连接、HTTP 报文解析、线程模型 | Tomcat（Servlet 容器） |
| Servlet 层 | Servlet 生命周期、Request/Response、Filter、Session | Tomcat（按 Jakarta Servlet 规范实现） |
| Web 框架层 | URL 路由、Controller、参数绑定、视图、拦截器 | **Spring MVC**（DispatcherServlet 本身就是一个 Servlet） |
| 应用基础设施层 | Bean 装配、事务、AOP、持久化、校验、安全、消息 | Spring 全家桶 |

注意 `DispatcherServlet` 这个名字：Spring MVC 的总入口**本身就是一个注册到 Tomcat 的 Servlet**。所以"Spring 不做 web 层"是错的——它做的是 web 层的上半截，下半截仍站在 Servlet 规范上。

### 3. Spring 6 之后：替代编程模型，消费底层规范

很多人以为 Spring Boot 和 Jakarta EE 是"你死我活"，实际上 Spring 6 / Boot 3 全量迁到 `jakarta.*` 包名后，分工是这样的：

- **直接消费的 Jakarta 规范**（底层由别人实现）：
  - Jakarta Servlet → Tomcat/Jetty 实现
  - Jakarta Persistence(JPA) → Hibernate 实现
  - Jakarta Bean Validation → Hibernate Validator 实现
  - Jakarta Annotations / Transaction 等 → Spring 对接
- **Spring 自研替代的部分**：
  - IoC/DI（替代 EJB 容器 / CDI 的定位）
  - 声明式事务（`@Transactional`，替代 EJB 容器管理事务，底层可接 JTA）
  - 安全模型（Spring Security 替代容器安全/EJB 安全）
  - 自动配置 + starter 依赖管理 + 内嵌容器（替代 EE 的部署模型）

***

## 四、Spring Boot 如何用一个 jar 对齐 EE 全部能力

### 1. 装配方向的反转（本文最重要的一张图）

```
Java EE 模型（应用薄，容器厚）
┌─────────────────────────────────────────────┐
│              完整应用服务器（厚）              │
│  WildFly：Servlet 容器 + EJB 容器 + JTA       │
│           + JPA + JMS + 安全 + JNDI ...       │
│  ┌──────┐ ┌──────┐                           │
│  │ war  │ │ ejb  │  ← 应用（薄，只放业务类）    │
│  └──────┘ └──────┘                           │
└─────────────────────────────────────────────┘
部署：打 ear/war → 投递到已运行的服务器

Spring Boot 模型（应用厚，容器薄）
┌─────────────────────────────────────────────┐
│        可执行 jar（一个自包含进程）            │
│  业务类 + Spring（IoC/TX/MVC/Security）       │
│   + Hibernate + Tomcat(内嵌,只取 Web 能力)    │
└─────────────────────────────────────────────┘
部署：java -jar（或做成 Docker 镜像），服务器是应用的一部分
```

### 2. 三件法宝让"库即能力"成立

1. **starter 依赖**：`spring-boot-starter-web` 一条依赖，自动拉入 Spring MVC + 内嵌 Tomcat + Jackson + 校验——EE 时代要手工装服务器、配 shared lib 的工作变成 Maven 坐标声明。
2. **自动配置**：类路径上出现什么库，就按条件装配什么 Bean（`@ConditionalOnClass` 等），替代 web.xml / application.xml 的手工装配。
3. **内嵌容器 + fat jar**：Tomcat 从"部署目标"降级为"一个 jar 依赖"，应用自身成为可独立启动的进程，每个微服务一个进程，与 Kubernetes"一个容器一个进程"模型天然吻合。

### 3. 能力对照：EE 给的，Boot 怎么给

| EE 能力 | EE 提供方式 | Spring Boot 对应 |
|---|---|---|
| HTTP/Servlet | 服务器内置 Servlet 容器 | 内嵌 Tomcat（starter-web），可换 Jetty/Undertow |
| 依赖注入 | EJB / CDI 容器 | Spring IoC（`@Component`/`@Autowired`） |
| 声明式事务 | EJB `@TransactionAttribute` / JTA | `@Transactional`（DataSource 事务，可接 JTA） |
| ORM 持久化 | JPA + 容器托管 EntityManager | Spring Data JPA + Hibernate |
| 参数校验 | Bean Validation | starter-validation（Hibernate Validator） |
| 安全 | 容器安全 / EJB 安全注解 | Spring Security |
| 消息 | JMS + MDB（消息驱动 Bean） | spring-jms / spring-kafka 等 |
| 配置/熔断/健康检查 | EE 本体没有（后由 MicroProfile 补） | Spring Boot 配置体系 + Actuator + Resilience4j/Spring Cloud |
| 打包部署 | ear/war 投到外置服务器 | 可执行 jar / Docker 镜像，内嵌容器 |

***

## 五、能力对照表

把三种技术形态放在一起看：

| 维度 | 传统 Java EE | 独立 Tomcat + Spring | Spring Boot |
|---|---|---|---|
| 打包物 | ear（内含 war + ejb jar） | war | 可执行 jar（fat jar） |
| 服务器位置 | 外置，预先安装运行 | 外置 Tomcat | 内嵌，随应用启动 |
| 进程模型 | 一服务器多应用 | 一 Tomcat 多 war | 一应用一进程 |
| 组件模型 | EJB（重） | Spring POJO | Spring POJO + 自动配置 |
| 事务 | JTA（容器管理） | Spring TX | Spring TX（可选 JTA） |
| 配置 | XML 部署描述符 | XML + 注解 | application.yml + 自动配置 |
| 规范关系 | 全套 Jakarta EE 实现 | Servlet 规范 + 自研其余 | 消费 `jakarta.*` 子集 + 自研其余 |
| 典型运行环境 | WebLogic/WildFly 虚机 | Tomcat 虚机 | Kubernetes/Docker 容器 |
| 当下定位 | 存量系统（金融/电信/政府） | 传统部署过渡形态 | 新项目主流 |

***

## 六、常见误解纠正（四个高频错误模型）

1. **"EAR 打的是普通 Java 项目"** → 错。EAR 是完整 EE 企业应用的专属格式，含 Web/EJB 多模块，只有完整应用服务器能加载；普通项目打 jar，Web 项目打 war。
2. **"Tomcat 是 jar 项目，提供 war 插槽"** → 模型反了。Tomcat 是 Servlet 容器产品；war 是它独立模式的主食而非可选插槽；jar 形态的 Tomcat（embed）是给应用内嵌用的，此时是容器被装进应用。
3. **"Spring 只做 web 以外的层"** → 错。Spring MVC 就是 Web 框架（路由/Controller/参数绑定），Spring 只把"连接与 Servlet 引擎"这层粗活外包给 Tomcat。
4. **"Spring Boot 抛弃了 EE 标准另搞一套"** → 不准确。Boot 替代的是 EJB/CDI 的编程模型和外置服务器的部署模型；Servlet/JPA/Validation 等底层契约在 Boot 3 里直接以 `jakarta.*` 消费，由 Tomcat、Hibernate 等规范实现产品支撑。

***

## 七、演进时间线

| 时间 | 事件 | 对部署模型的影响 |
|---|---|---|
| 1999 | J2EE 发布，Servlet/EJB 规范出现 | war/ear + 外置应用服务器模型确立 |
| 2002 | Rod Johnson《Expert One-on-One J2EE…》，Spring 雏形 | POJO + 轻量容器挑战 EJB |
| 2006 | J2EE 更名 Java EE（JDK 6 去 "2" 品牌） | — |
| 2014 | Spring Boot 1.0 发布 | 内嵌容器 + 可执行 jar，装配方向反转 |
| 2017 | Oracle 将 Java EE 移交 Eclipse 基金会 | 规范易主，更新重启 |
| 2020 | Jakarta EE 9 发布，`javax.*` → `jakarta.*`（商标所迫） | 史上最大规模包名断代 |
| 2022 | Spring Framework 6 / Spring Boot 3：JDK 17 + 全量 `jakarta.*` | Spring 与 Jakarta 新命名空间合流 |
| 2025 | Jakarta EE 11 发布（Core/Web/Full 分档）；Quarkus/Micronaut 在云原生场景扩张 | 规范层仍在；实现产品走向云原生与原生镜像 |

**主线一句话**：外置厚服务器（ear 时代）→ 轻量框架 + 外置容器（Spring + war）→ 内嵌容器自包含进程（Spring Boot jar）→ 云原生编译时优化（Quarkus/Micronaut 消费同一批 Jakarta 规范）。

***

## 八、权威锚点

**S 级：一手规范与文档**

- Jakarta EE 平台规范与各 Profile 定义：https://jakarta.ee/specifications/platform/ （ear/war 部署约定的权威出处见平台规范的 Packaging 章节）
- Jakarta Servlet 规范：https://jakarta.ee/specifications/servlet/ （Servlet 生命周期、部署结构 WEB-INF 约定）
- Spring Boot 参考文档（Executable Jar / Embedded Container / Starters 章节）：https://docs.spring.io/spring-boot/
- Tomcat 官方文档（Deployment、Embedded 章节）：https://tomcat.apache.org/

**A 级：经典书**

- 周志明《深入理解Java虚拟机》《凤凰架构》——Java EE 到 Spring Boot/云原生演进的中文系统梳理。
- Rod Johnson《Expert One-on-One J2EE Design and Development》（2002）——Spring 设计动机的原始出处。
- Craig Walls《Spring in Action》——Spring 编程模型的标准入门。

**B 级：行业现状**

- Eclipse Foundation《2025 Jakarta EE Developer Survey》——Jakarta EE/Spring 使用率、EE 11 采用率的一手调研。
- Quarkus / Micronaut 官方文档——同一批 Jakarta 规范在云原生（编译时装配、GraalVM 原生镜像）下的另一种实现路径。
