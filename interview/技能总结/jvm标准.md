# 先说核心一句话

> 面试网上那些 JVM 面试总结，**是别人咀嚼二次加工的结论**；**官方标准文档叫《The Java Virtual Machine Specification》JVMS（Java 虚拟机规范），是定义 JVM 的第一手权威来源**。
>
> &#x20;⚠️ 重要区分：
>
> &#x20;JVMS：**规定 JVM “必须是什么行为”（标准）**
>
> &#x20;OpenJDK 文档 / HotSpot 文档：**HotSpot 虚拟机具体怎么实现这个标准**（工程实现，面试里 GC、JIT、对象内存布局都在这一块，JVMS 不会写 G1/ZGC）
>
> &#x20;👉 资深 Java 面试，**JVMS 打底 + HotSpot 实现 + 实操工具，三者搭配**，不能只啃 JVMS，JVMS 不写 GC 收集器。

## 一、官方资料清单（标准来源，直接访问）

1. **JVMS 官方总入口**

   [https://docs.oracle.com/javase/specs/index.html](https://link.wtturl.cn/?target=https%3A%2F%2Fdocs.oracle.com%2Fjavase%2Fspecs%2Findex.html\&scene=im\&aid=582478\&lang=zh "autolink")**Oracle**

   &#x20;你可以选版本：**优先选你业务在用的版本，企业主流 JDK8 / JDK17**

- JDK8：JVMS8，PDF：[https://docs.oracle.com/javase/specs/jvms/se8/jvms8.pdf](https://link.wtturl.cn/?target=https%3A%2F%2Fdocs.oracle.com%2Fjavase%2Fspecs%2Fjvms%2Fse8%2Fjvms8.pdf\&scene=im\&aid=582478\&lang=zh "autolink")**Oracle**
- JDK17：JVMS17，HTML 在线版，阅读更方便

> JVMS 内容范围：
>
> &#x20;第 2 章 JVM 架构、运行时数据区（栈、堆、方法区）
>
> &#x20;第 4 章 class 文件格式
>
> &#x20;第 5 章 类加载、链接、初始化（双亲委派在这一章！）
>
> &#x20;第 6 章 字节码指令
>
> &#x20;线程 & 内存模型 JMM 在《Java 语言规范 JLS》第 17 章，**JVMS 本身不包含 JMM**

> 局限（非常关键，很多人踩坑）：
>
> &#x20;✅ JVMS 定义规范，规定 JVM**必须遵守的行为**
>
> &#x20;❌ **JVMS 不规定 GC 算法、不规定分代、不规定对象头布局、不规定 G1/ZGC、不写 JIT**。
>
> &#x20;GC、对象布局、STW 这些，属于**HotSpot 实现细节**，属于 OpenJDK 官方文档，不属于 JVMS 规范。
>
> &#x20;面试官问 G1、ZGC、对象头、逃逸分析，**不能只翻 JVMS，要看 OpenJDK 官方文档**

1. **OpenJDK 官方文档（HotSpot 实现，面试高频，第二权威）**

   [https://openjdk.org/groups/hotspot/](https://link.wtturl.cn/?target=https%3A%2F%2Fopenjdk.org%2Fgroups%2Fhotspot%2F\&scene=im\&aid=582478\&lang=zh "autolink")

   &#x20;里面包含 HotSpot GC、JIT、内存布局、JEP 提案（比如 ZGC 的 JEP）。

> JEP：JDK Enhancement Proposal，JDK 新特性官方提案文档，ZGC、虚拟线程这些，原始出处都是 JEP。

1. JMM（Java 内存模型）官方文档：《The Java Language Specification (JLS)》第 17 章，不是 JVMS。

> volatile、happens-before 全部在这里。

> 中文：**JVMS 没有官方中文版**。网上的《Java 虚拟机规范中文版》是社区翻译，翻译会有歧义，**核心定义必须对照英文原版**。

## 二、阅读策略：不需要通读整本 JVMS！（资深面试，重点章节 + 跳过章节）

### ✅ 重点精读章节（面试必考，对照官方原文，用来校正网上面试题错误结论）

1. Chapter 2: The Structure of the Java Virtual Machine
   - 运行时数据区：虚拟机栈、本地方法栈、堆、方法区、程序计数器。
   > 网上很多面试题会错误混淆 “方法区、元空间”，JVMS 定义方法区是**逻辑概念**；元空间是 HotSpot 在 JDK8 的物理实现。这就是面试高频坑，官方原文能帮你区分【规范定义】vs【HotSpot 实现】。
2. Chapter 5: Loading, Linking, and Initializing

   &#x20;类加载的 5 个阶段（加载、验证、准备、解析、初始化），双亲委派模型，**这一章是类加载问题的源头**。很多网上面试题对双亲委派描述是错的，以这一章为准。
3. Chapter4 class 文件：可以粗略看，看懂魔数、常量池即可，不用死背。

### ❌ 直接跳过（面试资深岗不需要精读）

- 全部字节码指令表 Chapter6，不用逐条背；会用 javap 看字节码即可。
- 规范里很底层的校验、class 文件详细结构，除非你做字节码框架，否则只做了解。

> 阅读方式：**先看国内靠谱书建立骨架（周志明《深入理解 Java 虚拟机》，这本书是基于 JVMS+HotSpot 写的，不是替代官方文档），遇到争议概念，翻 JVMS 原文校准。**
>
> &#x20;流程：看书建立理解 → 发现网上面试题说法冲突 → 打开 JVMS 原文查标准定义。
>
> &#x20;不是从头啃几百页英文规范。

## 三、学到什么程度，才算满足资深 Java 面试（P6\~P7）

分三层：**规范层 (JVMS)、HotSpot 实现层、实操层**

### 1）规范层（JVMS）

- 能分清：**JVM 规范定义的逻辑概念，和 HotSpot 具体实现的区别**

  &#x20;例子：方法区（规范逻辑） vs 永久代 (JDK7) / 元空间 (JDK8 HotSpot 实现)
- 能口述类加载、链接、初始化完整流程，知道双亲委派的目的，破坏双亲委派场景；原文定义，不是背诵网上总结。
- 运行时数据区，各个区域存储内容、OOM 的来源，**区分规范定义**

### 2）HotSpot 实现层（面试重点，JVMS 不包含）

- 内存：对象布局（对象头、markword、实例数据、对齐填充），逃逸分析，栈上分配
- GC：分代模型；G1、ZGC、CMS 原理，STW，各收集器适用场景、优缺点
- JIT：解释器 + C1/C2 编译器，分层编译
- JMM：happens-before 规则，volatile 语义（JLS）

### 3）实操层（资深面试**必须动手**，只看文档直接扣分）

> 面试官一定会问排查场景，**不动手，答出来就是背书**。

#### 必做实操清单（JDK 自带工具，不需要额外软件）

环境：JDK8 / JDK17，用`jps、jstack、jmap、jstat、jhat`，还有`javap`

1. javap：写简单 Java 代码，编译，看 class 字节码，验证常量池、指令。用来理解 class 文件。
2. 制造 OOM：写一段代码不停 new 对象，触发堆 OOM；
   - jstat 实时观察 GC 指标（YGC,FGC, 堆使用率）
   - jmap dump 堆快照
   - MAT（Memory Analyzer Tool）分析 dump，定位泄漏对象
3. 制造死锁：手写死锁代码，jstack 抓取线程栈，识别死锁。
4. 观察线程栈溢出：递归制造 StackOverflowError，理解虚拟机栈。
5. jstat 持续观察 G1 GC，看 GC 停顿、STW。

> 实操目标：
>
> &#x20;给你线上场景：**CPU 高、频繁 FullGC、OOM、线程死锁**，你能口述完整排查链路、工具使用顺序、看哪些指标，并且你**亲手复现过同类现象**。
>
> &#x20;这就是和只会背面试题的人拉开差距的关键点。

## 四、整套学习顺序（推荐）

1. 先用周志明《深入理解 Java 虚拟机》建立整体知识骨架（这本书是国内最好的 HotSpot 工程讲解，**不是官方，但是用来铺垫，方便看懂官方文档**）
2. 遇到概念有歧义（网上多个版本说法），打开 JVMS 原文核对定义。
   > 例：网上有人争论 “类加载的准备阶段是否赋 0 值”，直接翻 JVMS 第 5 章原文，一句话终结争议。
3. 动手实操，复现 OOM、死锁，使用 JDK 工具，看懂日志。
4. 然后去看 OpenJDK JEP 文档，学习 G1/ZGC 等收集器原理。
5. 最后，用面试场景题检验：线上故障排查、GC 调优场景。

## 五、避坑提醒

1. 不要把 JVMS 规范 = HotSpot 实现。**规范只定义行为，不限定内部实现**。

   &#x20;例如 JVMS 没有规定堆要分代，分代只是 HotSpot 的实现。面试这里很容易被连环追问挖坑。
2. 不要死磕英文规范，把大量时间耗在字节码细节，性价比极低。
3. 网上很多 JVM 面试总结，是简化、甚至有错误的结论；**官方文档是用来校验真伪，不是用来入门**。

## 六、我们下一步怎么开始

两个选项：

&#x20;A：先从【运行时数据区】开始，对照 JVMS 原文，把每个区域的**规范定义 + HotSpot 实现**一次性梳理，同时附带对应的实操代码。

&#x20;B：直接写一段代码，制造 OOM，完整走一遍 jstat+jmap+MAT 实操流程。

你想选哪一个？
