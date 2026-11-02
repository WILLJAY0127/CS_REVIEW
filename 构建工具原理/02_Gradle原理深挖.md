# 02. Gradle 原理深挖

> 核心理解：**Maven 是固定流水线，Gradle 是可自由编排的 DAG 任务图**。

---

## 一、Gradle 与 Maven 的核心差异

### 一张表看懂

| 维度 | Maven | Gradle |
|------|-------|--------|
| **核心模型** | 固定生命周期（clean → compile → test → package） | 灵活的 Task DAG（有向无环图） |
| **配置语言** | XML（啰嗦、声明式） | Groovy / Kotlin DSL（像写代码） |
| **执行顺序** | 阶段写死，顺序固定 | DAG 拓扑排序，能并行 |
| **编译策略** | 全量（每次重编所有） | 增量（只编改了的+依赖它的） |
| **缓存** | 无 | Build Cache（本地/远程都有） |
| **灵活度** | 约定优先，改起来要写插件 | 约定保留，改起来是写 DSL |
| **学习曲线** | 平缓（固定流程容易理解） | 陡峭（DSL + DAG 需要理解） |

### 为什么 Gradle 快？

```
Maven 每次构建：
  compile → test → package  (全量，每一步都重新来)

Gradle 每次构建：
  1. 先看 DAG：哪些 Task 改了输入？
  2. compileJava：上次编译的 .class 还在吗？.java 有没改？
     → 没改就跳过！（增量构建）
  3. test：上次测试过没？依赖的 class 有没变？
     → 没变就跳过！
  4. package：class 和资源有没变？
     → 没变就跳过！

更狠的：Build Cache
  → 我这台机器跳过的编译结果，另一台机器也能直接用
  → 远程缓存：CI 机器编过的，本地开发也能直接拿
```

---

## 二、Gradle 的核心模型：Project + Task

### 只有两个核心概念

```
Gradle 构建 = 一个或多个 Project（项目）
Project = 一组 Task（任务）
Task 之间有依赖关系（形成 DAG）
```

### DAG（有向无环图）是什么？

**有向**：A → B 表示 B 依赖 A
**无环**：不能出现 A → B → A（死循环，Gradle 启动时就会报错）

```
示例：一个项目的 Task 依赖图

     clean        ← 独立任务（没依赖）
       |
    compileJava   ← 依赖 clean
       |
    compileTest   ← 依赖 compileJava
       |
    test          ← 依赖 compileTest
       |
    jar           ← 依赖 test
```

Gradle 启动时：
1. 收集所有 Task 和它们的 `dependsOn` 关系
2. 构建 DAG
3. 拓扑排序算出执行顺序
4. **没有依赖关系的 Task 可以并行执行！**

### Gradle vs Maven：执行顺序对比

```
Maven（固定流水线）：
  validate → compile → test → package → install
  每个阶段必须等前面的完成，无法并行

Gradle（DAG 并行）：
  compileJava  ──→ test
  compileTest  ──┘
  这两个 compile 是独立的，可以同时跑！
```

---

## 三、Gradle 构建的三个阶段

### 这是理解 Gradle 的关键！

```
┌──────────────────────────────────────────────────────────┐
│                     Gradle 构建流程                       │
│                                                          │
│  Phase 1: 初始化（Initialization）                        │
│    → 读 settings.gradle，确定有哪些 Project              │
│    → 为每个 Project 创建对应的对象                        │
│                                                          │
│  Phase 2: 配置（Configuration）                            │
│    → 读每个 build.gradle                                  │
│    → 执行里面所有的配置代码（注意：这里不执行 Task！）       │
│    → 构建 DAG（Task 的 dependsOn 关系在这里确定）          │
│                                                          │
│  Phase 3: 执行（Execution）                                │
│    → 根据 DAG 拓扑排序执行 Task                           │
│    → 执行增量判断 + Build Cache 检查                      │
└──────────────────────────────────────────────────────────┘
```

### 为什么分三个阶段？

因为 Gradle 的 `build.gradle` 里写的**不只是配置声明，还有可执行代码**！

```groovy
// build.gradle（Groovy DSL）

// ===== 这些是配置代码，在 Phase 2 执行 =====
plugins {
    id 'java'    // 应用 java 插件，注册了 compileJava 等 Task
}

group = 'com.example'
version = '1.0.0'

dependencies {
    implementation 'org.springframework:spring-core:5.3.39'
}

// ===== 这段代码在 Phase 2 就执行了 =====
// 它是配置代码，用来定义一个新 Task
task hello {
    // 闭包里的配置代码在 Phase 2 执行
    group = 'custom'
    description = '一个示例任务'
    
    // ===== 这段是 Task 的 action，在 Phase 3 执行 =====
    doLast {
        println "Hello World! Version: ${version}"
    }
}

// Task 依赖关系也在 Phase 2 确定
hello.dependsOn compileJava
```

### 这个分阶段模型有什么好处？

```
Maven：配置是纯 XML 声明，没法动态控制
Gradle：配置是 Groovy/Kotlin 代码，可以动态决定

比如：只在某个条件下才加一个 Task
task deploy {
    doLast {
        // 动态逻辑
        if (project.hasProperty('env')) {
            println "部署到 ${project.env}"
        }
    }
}
```

---

## 四、Gradle 常用 DSL 写法

### build.gradle.kts（Kotlin DSL，更有类型提示）

```kotlin
// 插件
plugins {
    java
    `maven-publish`
}

// 项目属性
group = "com.example"
version = "1.0.0"

// Java 版本配置
java {
    sourceCompatibility = JavaVersion.VERSION_1_8
    targetCompatibility = JavaVersion.VERSION_1_8
}

// 仓库
repositories {
    mavenCentral()
    maven { url = uri("https://maven.aliyun.com/repository/public") }
}

// 依赖（注意 scope 名字变了）
dependencies {
    implementation("org.springframework:spring-core:5.3.39")
    compileOnly("org.projectlombok:lombok:1.18.30")
    runtimeOnly("mysql:mysql-connector-java:8.0.33")
    testImplementation("junit:junit:4.13.2")
}

// 自定义 Task
tasks.register<Jar>("fatJar") {
    archiveClassifier.set("all")
    manifest {
        attributes["Main-Class"] = "com.example.Main"
    }
    from(configurations.runtimeClasspath.get().map { if (it.isDirectory) it else zipTree(it) })
    with(tasks.jar.get())
}
```

### build.gradle（Groovy DSL）

```groovy
plugins {
    id 'java'
}

group = 'com.example'
version = '1.0.0'

java {
    sourceCompatibility = '1.8'
    targetCompatibility = '1.8'
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework:spring-core:5.3.39'
    compileOnly 'org.projectlombok:lombok:1.18.30'
    testImplementation 'junit:junit:4.13.2'
}

// 自定义 Task
task fatJar(type: Jar) {
    archiveClassifier = 'all'
    manifest {
        attributes 'Main-Class': 'com.example.Main'
    }
    from { configurations.runtimeClasspath.collect { it.isDirectory() ? it : zipTree(it) } }
    with jar
}
```

---

## 五、Gradle 的依赖 scope 对照

| Gradle scope | Maven scope | 什么时候用 |
|-------------|------------|-----------|
| `implementation` | `compile` | 主要依赖，编译和运行都要用 |
| `api` | （无） | 对外暴露的依赖（多模块时用） |
| `compileOnly` | `provided` | 编译时需要，运行时环境提供 |
| `runtimeOnly` | `runtime` | 编译时不需要，运行时才要 |
| `testImplementation` | `test` | 只在测试时用 |
| `testCompileOnly` | — | 测试时编译需要，运行不需要 |
| `testRuntimeOnly` | — | 测试运行时才需要 |

### implementation vs api（Gradle 独有的）

这是 Gradle 对 Maven scope 的一个重要改进：

```groovy
// implementation：依赖不暴露给下游
// A 模块的 implementation 依赖，B 模块依赖 A 后看不到这个依赖
implementation 'org.springframework:spring-core'

// api：依赖暴露给下游
// A 模块的 api 依赖，B 模块依赖 A 后也能看到这个依赖
api 'org.springframework:spring-web'
```

好处：**减少传递依赖泄露**，加速编译。

---

## 六、Gradle 的增量构建原理

### 为什么改一个文件只编译一个？

```
Gradle 为每个 Task 记录两个东西：
  输入（inputs）：Task 执行需要的数据
  输出（outputs）：Task 执行产生的数据

compileJava Task：
  输入 = src/main/java/ 下所有 .java 文件 + classpath 上的依赖 jar
  输出 = build/classes/java/main/ 下所有 .class 文件

Gradle 在 Task 第一次执行后，把输入的 hash 存起来
下次构建时：
  1. 算一遍输入的 hash
  2. 和上次存的比
  3. 完全一样 → 跳过！
  4. 有变化 → 只重新编译变化的文件 + 依赖它们的文件
```

### Build Cache 更进一步

```
增量构建解决的是：本机没改的代码跳过
Build Cache 解决的是：别的机器编过的代码直接拿

工作流程：
  1. 某台机器跑 compileJava，把 .class 打包进缓存
  2. 另一台机器构建同一个项目
  3. 它的 compileJava 输入完全一样（同样的 .java + 同样的依赖）
  4. 直接从缓存拿 .class，不用自己编译了！
```

### 怎么启用 Build Cache？

```groovy
// gradle.properties
org.gradle.caching=true
```

---

## 七、Gradle 多模块：settings.gradle

### 目录结构

```
root/
├── settings.gradle.kts         ← Gradle 的根配置，声明有哪些模块
├── build.gradle.kts            ← 根构建脚本
├── common/
│   └── build.gradle.kts
├── service/
│   └── build.gradle.kts
└── web/
    └── build.gradle.kts
```

### settings.gradle.kts

```kotlin
// 指定根项目名
rootProject.name = "my-root-project"

// 声明子模块
include("common", "service", "web")
```

### 根 build.gradle.kts

```kotlin
// 根项目用 buildscript 管理插件版本
plugins {
    id("java") apply false       // apply false = 根项目自己不用，子项目用
}

// 配置所有子项目
subprojects {
    apply(plugin = "java")
    
    group = "com.example"
    version = "1.0.0"
    
    repositories {
        mavenCentral()
    }
    
    // 子项目间依赖声明
    dependencies {
        // service 和 web 模块自动能依赖 common
        // 写在 subprojects 里表示所有子项目都能引用
    }
}

// 也可以用 allprojects 配置根项目 + 所有子项目
allprojects {
    // ...
}
```

### 子项目间依赖

```kotlin
// service/build.gradle.kts
dependencies {
    // 引用兄弟模块
    implementation(project(":common"))
    
    implementation("org.springframework:spring-core:5.3.39")
}
```

### Gradle 的模块依赖自动排序

```bash
# 和 Maven 一样，Gradle 自动按 dependsOn 排序
./gradlew clean build
# 但 Gradle 可以并行编译没有依赖关系的模块！
# common 和 其他没有依赖的模块可以同时编
```

---

## 八、Gradle 命令行速查

| 命令 | 用途 |
|------|------|
| `./gradlew tasks` | 列出所有 Task |
| `./gradlew build` | 完整构建（compile + test + jar） |
| `./gradlew clean` | 清空 build/ 目录 |
| `./gradlew jar` | 只打包 |
| `./gradlew test` | 只跑测试 |
| `./gradlew compileJava` | 只编译 main 代码 |
| `./gradlew dependencies` | 看依赖树 |
| `./gradlew :service:build` | 只构建 service 模块 |
| `./gradlew build --parallel` | 并行构建 |
| `./gradlew build --rerun-tasks` | 强制重新构建（跳过增量检查） |
| `./gradlew build --no-build-cache` | 跳过 Build Cache |

### Gradle Wrapper（强烈建议用）

```bash
# 生成 Wrapper
gradle wrapper --gradle-version 8.5

# 之后用 ./gradlew（或 gradlew.bat on Windows）
# 好处：
# 1. 项目自带 Gradle 版本，不用全局安装
# 2. 团队里每个人用的 Gradle 版本一致
# 3. CI 机器上也不需要预装 Gradle
```

---

## 九、Gradle 与 Maven 互转

### Maven → Gradle

```bash
# 在 Maven 项目根目录执行
gradle init --type pom

# 它会：
# 1. 读取 pom.xml
# 2. 生成 build.gradle + settings.gradle
# 3. 把依赖、插件、scope 都自动转好
```

### Gradle → Maven 仓库

Gradle 项目可以直接发布到 Maven 仓库：

```kotlin
plugins {
    `maven-publish`
}

publishing {
    publications {
        create<MavenPublication>("maven") {
            groupId = "com.example"
            artifactId = "my-app"
            version = "1.0.0"
            from(components["java"])
        }
    }
    repositories {
        maven {
            url = uri("https://your-nexus.com/repo/maven-public")
            credentials {
                username = "user"
                password = "pass"
            }
        }
    }
}
```

---

## 十、Gradle 总结

| 概念 | 一句话 |
|------|--------|
| DAG | Task 之间的依赖图，拓扑排序执行，可并行 |
| Project | 一个 Gradle 模块（根项目或子项目） |
| Task | 一个具体动作（编译、测试、打包...） |
| 三阶段 | 初始化（确定模块）→ 配置（执行 DSL）→ 执行（跑 Task） |
| 增量构建 | 只重新执行输入有变化的 Task |
| Build Cache | 跨机器复用编译结果 |
| implementation vs api | Gradle 独有的，控制依赖是否暴露给下游 |
| Wrapper | 项目自带 Gradle 版本，团队统一 |

---

## 十一、Maven vs Gradle 最终对比

| 场景 | 推荐 | 理由 |
|------|------|------|
| **新项目** | Gradle | 快、灵活、未来主流 |
| **旧项目已用 Maven** | 继续用 Maven | 迁移成本高，不值得 |
| **学习目的** | 先 Maven 再 Gradle | Maven 帮你建立"依赖+生命周期"心智模型 |
| **多模块大项目** | Gradle | 增量+并行，速度差距明显 |
| **企业传统 Java** | 可能是 Maven | 历史包袱、团队习惯 |
| **Android 项目** | 必须 Gradle | Android Studio 强制用 Gradle |
| **CI/CD** | 都行 | 但 Gradle 的 Build Cache 在 CI 上优势巨大 |
