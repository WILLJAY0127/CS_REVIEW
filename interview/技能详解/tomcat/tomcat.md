# Tomcat书单（适配你资深Java面试、分层学习思路，区分【原理】【实操】【官方基准】）
> 你的学习思路：**先契约/规范，再架构，再源码，配合实操验证**，和JVM、Spring保持同一套学习方法论

## 1. 《深入剖析Tomcat》（How Tomcat Works）⭐核心必看
- 原著：*How Tomcat Works*，机械工业出版社，曹旭东译
- 特点：**最适合建立底层模型**。不直接扔大堆源码，而是带着你**从零手写简易版Servlet容器**，一点点实现Connector、Container、Pipeline、Lifecycle。
- 局限：基于Tomcat4/5，版本很老；NIO、APR、新版类加载器这些新特性没有。
- 适合：理解**Servlet容器本质**，搞懂请求流转、组件生命周期，面试底层原理的基石。

## 2. 《Tomcat架构解析》刘光瑞 ⭐国内首选（Tomcat7/8）
- 人民邮电出版社
- 特点：国内写Tomcat内核最好的一本。覆盖Server→Service→Connector→Engine→Host→Context完整组件；Pipeline-Valve、类加载、性能调优、集群、和Nginx集成。
- 局限：基于Tomcat7、8，Tomcat9/10的Jakarta包改名、新NIO改进没有。
- 适合：看完《深入剖析Tomcat》之后，用来补现代Tomcat完整架构，面试高频知识点（类加载、线程模型、调优）。

## 3. 《Tomcat内核设计剖析》汪建
- 聚焦源码，偏Tomcat8，讲解源码阅读思路，组件、请求处理、线程池、内存模型。
- 适合：**准备动手debug源码**时参考；缺点文字密度高，入门略难。

## 4. 《Tomcat与Java Web开发技术详解》孙卫琴
- 偏应用层，Tomcat6，讲部署、web.xml、Servlet/JSP开发。
- 适合：如果你需要补齐Servlet规范+Tomcat基础使用；**不适合深挖内核**。

## 5. OReilly《Tomcat: The Definitive Guide》（Tomcat权威指南）
- 英文原版，偏运维部署、配置、安全，内核讲得浅。适合运维侧，**不推荐用来准备Java后端底层面试**。

# ✅ 最高优先级【官方文档】—— 你的“官方基准”，优先级高于所有书籍
> 和JLS、JVMS是一个定位，**权威标准，没有版本过时问题**
https://tomcat.apache.org/
重点看三块：
1. User Guide：使用、部署基础
2. Configuration Reference：server.xml所有配置项定义（最核心参考）
3. Architecture文档：Tomcat官方架构文档，描述组件、启动流程、请求链路（**这就是官方的组件契约**）

配套：**Servlet规范（Jakarta Servlet Spec）**，这是Tomcat必须遵守的契约，和JLS一样，Tomcat只是这个规范的实现。
> 学习分层（延续你之前的抽象层级思想）
```
Jakarta Servlet规范（契约层，最高层）
        ↓
Tomcat官方架构文档（Tomcat自身组件契约）
        ↓
书籍：How TomcatWorks / Tomcat架构解析（原理模型）
        ↓
Tomcat源码（HotSpot一样，具体实现层）
```

# 📚推荐学习顺序（适配面试）
1. 先读 **Tomcat官方Architecture文档**，建立组件模型（Server、Service、Connector、Container、Lifecycle）
2. 《深入剖析Tomcat》，理解容器本质、Pipeline，建立简易实现模型
3. 《Tomcat架构解析》，补Tomcat8现代特性：NioEndPoint、线程池、类加载、集群、调优
4. 动手实操：下载Tomcat8.5/9，改server.xml，抓包，debug源码，验证书本上的结论（就像你“触摸JVM”一样，触摸Tomcat）

# 面试重点（看完上面内容后，要掌握的）
- Connector（BIO/NIO/NIO2/APR），Endpoint线程模型
- Container层级：Engine/Host/Context/Wrapper，Pipeline-Valve责任链
- Tomcat类加载器（打破双亲委派，面试高频）
- Lifecycle生命周期、启动流程
- 请求完整流转：accept → 解析request → pipeline处理 → response输出
- 性能调优参数、常见坑（线程池、连接数、静态资源）

> 补充提醒：书籍都会版本滞后，**以官方文档+Servlet规范作为真理标准，书籍只是帮你理解实现模型**，和你学习JVM思路完全一致。

你想，我们可以直接从Tomcat架构文档的组件模型开始，搭一套分层模型吗？