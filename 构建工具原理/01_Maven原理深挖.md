# 01. Maven 原理深挖

> 核心理解：**约定 + 坐标 + 生命周期 + 插件**，这四个是 Maven 的骨架。

---

## 一、POM 模型：Maven 的"大脑"

### POM = Project Object Model

Maven 启动的第一件事，就是读 `pom.xml`。这个文件是整个构建的**唯一真相源**。

### pom.xml 的最小骨架

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="...">

  <!-- ========= 1. 坐标（GAV）：我是谁 ========= -->
  <groupId>com.example</groupId>          <!-- 组织名，反域名 -->
  <artifactId>my-app</artifactId>        <!-- 项目名 -->
  <version>1.0.0-SNAPSHOT</version>      <!-- 版本号 -->
  <packaging>jar</packaging>             <!-- 产出格式：jar/war/pom -->

  <!-- ========= 2. 属性：可复用的变量 ========= -->
  <properties>
    <java.version>1.8</java.version>
    <spring.version>5.3.39</spring.version>
  </properties>

  <!-- ========= 3. 依赖：我需要谁 ========= -->
  <dependencies>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-core</artifactId>
      <version>${spring.version}</version>
    </dependency>
  </dependencies>

  <!-- ========= 4. 插件：怎么干活 ========= -->
  <build>
    <plugins>
      <plugin>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.11.0</version>
        <configuration>
          <source>${java.version}</source>
          <target>${java.version}</target>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

### 坐标 GAV 是什么？为什么用它？

```
坐标 = groupId : artifactId : version

类比：快递地址
  groupId = 省 + 市（组织边界）
  artifactId = 街道 + 门牌号（具体项目）
  version = 第几版（确保你拿的是正确的那个）
```

**为什么用坐标而不是直接用 jar 文件名？**

因为：
1. **唯一性**：全球不会有两个 `org.springframework:spring-core:5.3.39`
2. **可搜索**：Maven 可以根据坐标去中央仓库精准定位
3. **解决版本管理**：同一个 artifactId 的不同 version 是不同的东西

---

## 二、Maven 的生命周期：固定流水线

### 三套生命周期

```
┌─────────────────────────────────────────────────────────┐
│ Maven 有 3 套独立的生命周期，每套包含多个阶段（Phase）      │
│                                                         │
│ clean 生命周期（清理）                                    │
│   pre-clean → clean → post-clean                        │
│                                                         │
│ default 生命周期（构建核心，最重要）                       │
│   validate → initialize → generate-sources → ...        │
│   → compile → test → package → verify → install → deploy │
│                                                         │
│ site 生命周期（生成文档，不常用）                           │
│   pre-site → site → post-site → site-deploy              │
└─────────────────────────────────────────────────────────┘
```

### default 生命周期各阶段在干什么？

| 阶段 | 干什么 | 关键产物 |
|------|--------|---------|
| validate | 校验 pom.xml 没问题 | 无 |
| **compile** | 编译 main 源码 | `target/classes/*.class` |
| test-compile | 编译 test 源码 | `target/test-classes/*.class` |
| **test** | 跑单元测试 | `target/surefire-reports/` |
| **package** | 打包成 jar/war | `target/my-app-1.0.0.jar` |
| verify | 运行集成测试 | 验证报告 |
| **install** | 安装到本地仓库 | `~/.m2/repository/.../my-app-1.0.0.jar` |
| **deploy** | 部署到远程仓库 | N/A（服务器上） |

### 关键规则：你指定的阶段，前面的阶段会自动执行

```bash
# 只跑 compile？那前面的 validate 会自动先跑
mvn compile
# 等价于：validate → compile

# 跑 test？compile 和 test-compile 都会自动先跑
mvn test
# 等价于：validate → initialize → ... → compile → test-compile → test

# 跑 install？整条链都跑一遍
mvn install
# validate → ... → compile → test → package → verify → install
```

**Maven 的设计思路：你只要说"我要哪个结果"，它自动算好要经过哪些阶段。**

### clean 生命周期的特殊之处

`mvn clean` 是独立的生命周期，**每次跑构建前建议先 clean**：

```bash
mvn clean install
# 先执行 clean 生命周期（删掉 target/）
# 再执行 default 生命周期到 install
```

---

## 三、插件机制：谁在真正干活？

### 生命周期是流程，插件才是执行者

**阶段（Phase）本身不干活，它是个"时间点标记"。真正执行的是插件的 goal（目标）。**

```
阶段（Phase）= 流水线的工位编号
插件（Plugin）= 工位上的机器人
Goal = 机器人能做的具体动作
```

### Maven 的内置插件（核心插件）

| 插件 | 默认绑定阶段 | 干的事 |
|------|-------------|--------|
| maven-compiler-plugin | compile / test-compile | 调用 javac 编译 |
| maven-surefire-plugin | test | 跑 JUnit 测试 |
| maven-jar-plugin | package | 把 class 打成 jar |
| maven-install-plugin | install | 复制 jar 到本地仓库 |
| maven-deploy-plugin | deploy | 上传 jar 到远程仓库 |
| maven-resources-plugin | resources / testResources | 复制资源文件 |

### 手动调用插件的 goal

你可以**不经过生命周期**，直接调插件的 goal：

```bash
# 只编译（等价于 mvn compile，因为 compiler:compile 绑定了 compile 阶段）
mvn compiler:compile

# 自定义编译某个东西（需要在 pom.xml 里配置插件参数）
mvn compiler:compile

# 跑指定测试
mvn surefire:test -Dtest=TestA
```

### 自定义插件行为

```xml
<build>
  <plugins>
    <plugin>
      <artifactId>maven-compiler-plugin</artifactId>
      <configuration>
        <!-- 改编译的 JDK 版本 -->
        <source>1.8</source>
        <target>1.8</target>
        <!-- 加编译参数 -->
        <encoding>UTF-8</encoding>
      </configuration>
    </plugin>

    <!-- 自定义打包：把所有依赖打进一个 fat jar -->
    <plugin>
      <artifactId>maven-assembly-plugin</artifactId>
      <configuration>
        <archive>
          <manifest>
            <mainClass>com.example.Main</mainClass>
          </manifest>
        </archive>
        <descriptorRefs>
          <descriptorRef>jar-with-dependencies</descriptorRef>
        </descriptorRefs>
      </configuration>
      <executions>
        <execution>
          <phase>package</phase>
          <goals>
            <goal>single</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

---

## 四、依赖管理：Maven 最复杂的部分

### 依赖的两个核心概念

```
1. 传递依赖（Transitive Dependency）
   A 依赖 B，B 依赖 C → 你引入 A，C 自动进来
   
2. 依赖范围（scope）
   这个依赖在什么时候用？编译时？测试时？运行时？
```

### scope 完整对照表

| scope | 编译 | 测试编译 | 运行 | 打包 | 什么时候用 |
|-------|------|---------|------|------|-----------|
| `compile`（默认） | ✅ | ✅ | ✅ | ✅ | 主要依赖，到处都要用 |
| `provided` | ✅ | ✅ | ❌ | ❌ | 容器/环境会提供的（servlet-api、lombok） |
| `runtime` | ❌ | ✅ | ✅ | ✅ | 编译时不需要，运行时才需要（JDBC 驱动） |
| `test` | ❌ | ✅ | ❌ | ❌ | 只有测试时用（junit、mockito） |
| `import` | — | — | — | — | 只在 dependencyManagement 里用（BOM） |

### 传递依赖带来的版本冲突

```
你的项目 A
  ├── 直接依赖: log4j:1.2.17（你自己想用的）
  └── 依赖 commons-io:2.11.0
        └── 传递依赖: log4j:1.2.14（commons-io 需要的）

问题：到底用 1.2.14 还是 1.2.17？
```

### Maven 的版本冲突解决规则（按优先级）

**规则 1：路径最近优先**

```
A → B → log4j:1.2.14   （深度 2）
A → log4j:1.2.17       （深度 1）→ 用这个！
```

**规则 2：同深度时第一声明优先**

```xml
<!-- 两个直接依赖都带 log4j，谁先写用谁 -->
<dependencies>
  <dependency>
    <groupId>commons-io</groupId>  <!-- 先写 -->
    <artifactId>commons-io</artifactId>
  </dependency>
  <dependency>
    <groupId>another-lib</groupId>  <!-- 后写 -->
    <artifactId>another-lib</artifactId>
  </dependency>
</dependencies>
```

**规则 3：手动排除**

```xml
<dependency>
  <groupId>commons-io</groupId>
  <artifactId>commons-io</artifactId>
  <exclusions>
    <!-- 明确告诉 Maven：把这个传递依赖排除掉 -->
    <exclusion>
      <groupId>log4j</groupId>
      <artifactId>log4j</artifactId>
    </exclusion>
  </exclusions>
</dependency>
<!-- 然后自己显式声明想要的版本 -->
<dependency>
  <groupId>log4j</groupId>
  <artifactId>log4j</artifactId>
  <version>1.2.17</version>
</dependency>
```

### 怎么看依赖树？

```bash
# 打印完整的依赖树，看谁引入了谁
mvn dependency:tree

# 只看某个具体依赖
mvn dependency:tree -Dincludes=log4j:log4j

# 打印详细冲突信息
mvn dependency:tree -Dverbose
```

### dependencyManagement：版本统一管理

父 pom 里用 `<dependencyManagement>` 统一管版本，子 pom 里只用写 GAV 不写 version：

```xml
<!-- 父 pom -->
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-core</artifactId>
      <version>5.3.39</version>
    </dependency>
    <!-- 所有子模块的 spring 版本在这里统一 -->
  </dependencies>
</dependencyManagement>

<!-- 子 pom -->
<dependencies>
  <dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-core</artifactId>
    <!-- 不用写 version，从父 pom 继承 -->
  </dependency>
</dependencies>
```

### BOM（Bill of Materials）

Spring Boot 的做法：**提供一个 BOM pom，里面把所有依赖版本都定好了**。

```xml
<!-- 引入 Spring Boot BOM -->
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-dependencies</artifactId>
      <version>2.7.18</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<!-- 然后你随便加 spring 的依赖，都不用写版本号 -->
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <!-- 版本号从 BOM 里继承 -->
  </dependency>
</dependencies>
```

---

## 五、仓库机制：依赖从哪来？

### 三级仓库搜索顺序

```
1. 本地仓库 ~/.m2/repository
   → 先看自己家有没有
   
2. 私服（Nexus / Artifactory / 阿里云镜像）
   → 公司内部统一代理，加速下载
   
3. 中央仓库 repo.maven.apache.org
   → 全球公共仓库，绝大多数开源库都在这
```

### 配置镜像加速（国内必须配）

`~/.m2/settings.xml`：

```xml
<settings>
  <mirrors>
    <mirror>
      <id>aliyun</id>
      <mirrorOf>central</mirrorOf>
      <url>https://maven.aliyun.com/repository/public</url>
    </mirror>
  </mirrors>
</settings>
```

### 依赖缓存机制

- 下载过一次的 jar 会存在 `~/.m2/repository/`
- 下次构建直接用，不联网
- SNAPSHOT 版本每次构建会检查更新（可强制更新：`mvn clean install -U`）

---

## 六、多模块项目：父 pom + 子模块

### 目录结构

```
parent/
├── pom.xml                    ← 父 pom（packaging=pom）
├── common/
│   └── pom.xml                ← 子模块 common
├── service/
│   └── pom.xml                ← 子模块 service
└── web/
    └── pom.xml                ← 子模块 web
```

### 父 pom

```xml
<!-- parent/pom.xml -->
<project>
  <groupId>com.example</groupId>
  <artifactId>parent</artifactId>
  <version>1.0.0</version>
  <packaging>pom</packaging>       <!-- 关键：pom 类型不产生 jar -->

  <modules>
    <module>common</module>
    <module>service</module>
    <module>web</module>
  </modules>

  <!-- 版本统一管理 -->
  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>5.3.39</version>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <!-- 公共插件配置 -->
  <build>
    <pluginManagement>
      <plugins>
        <plugin>
          <artifactId>maven-compiler-plugin</artifactId>
          <configuration>
            <source>1.8</source>
            <target>1.8</target>
          </configuration>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>
</project>
```

### 子 pom 继承父

```xml
<!-- common/pom.xml -->
<project>
  <parent>
    <groupId>com.example</groupId>
    <artifactId>parent</artifactId>
    <version>1.0.0</version>
    <!-- 子模块的相对路径 -->
    <relativePath>../pom.xml</relativePath>
  </parent>

  <!-- 不用再写 groupId / version，从父继承 -->
  <artifactId>common</artifactId>   <!-- 只有 artifactId 需要自己写 -->

  <dependencies>
    <!-- 用父 pom 里 dependencyManagement 定义好的版本 -->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-core</artifactId>
      <!-- 不用写 version！ -->
    </dependency>
  </dependencies>
</project>
```

### 子模块间互相依赖

```xml
<!-- service/pom.xml -->
<dependencies>
  <dependency>
    <groupId>com.example</groupId>
    <artifactId>common</artifactId>    <!-- 依赖兄弟模块 -->
    <version>${project.version}</version>  <!-- 用当前父版本 -->
  </dependency>
</dependencies>
```

### 多模块构建顺序

```bash
# 在父目录跑，Maven 自动算好模块间的依赖顺序
mvn clean install
# 先编 common（无依赖）
# 再编 service（依赖 common）
# 最后编 web（依赖 service）
```

---

## 七、Maven 命令行速查

| 命令 | 等价于 | 用途 |
|------|--------|------|
| `mvn clean` | clean 生命周期 | 清空 target/ |
| `mvn compile` | default 到 compile | 只编译 main 代码 |
| `mvn test` | default 到 test | 编译 + 跑测试 |
| `mvn package` | default 到 package | 编译 + 测试 + 打包 |
| `mvn install` | default 到 install | 打包 + 安装到本地仓库 |
| `mvn deploy` | default 到 deploy | 安装 + 部署到远程仓库 |
| `mvn clean install` | clean + default 到 install | 最常用的完整构建 |
| `mvn dependency:tree` | — | 看依赖树 |
| `mvn dependency:resolve` | — | 下载所有依赖到本地 |
| `mvn -DskipTests package` | package 但跳过测试 | 不想跑测试时用 |
| `mvn -U clean install` | install + 强制更新快照 | 快照版本更新时用 |
| `mvn -pl service -am install` | 只编 service 及它依赖的模块 | 大项目局部构建 |

---

## 八、Maven 总结

| 概念 | 一句话 |
|------|--------|
| POM | 构建的唯一配置，回答"我是谁、我要什么、我要产出什么" |
| GAV | 坐标，全球唯一标识一个项目 |
| 生命周期 | 固定流水线：clean / default / site |
| Phase | 流水线上的工位编号，本身不干活 |
| Plugin + Goal | 工位上的机器人，真正执行动作 |
| scope | 依赖在编译/测试/运行时是否需要 |
| 传递依赖 | A 依赖 B 依赖 C，C 自动进来 |
| 版本调解 | 路径最近优先 → 第一声明优先 → 手动排除 |
| 仓库 | 本地 → 私服 → 中央，三级搜索 |
| BOM | 统一管理一批依赖版本的 pom |
