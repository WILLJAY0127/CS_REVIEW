# CS61C Fall 2020 作业导航与公开题库

> 课程：UC Berkeley CS61C Great Ideas in Computer Architecture (Machine Structures)
> 学期：Fall 2020（Dan Garcia / Borivoje Nikolic，疫情线上学期，全程 RISC-V）
> 官方归档：https://www-inst.eecs.berkeley.edu/~cs61c/fa20/
> 配套知识体系：上级目录 [CS61C_知识库总览.md](file:///d:/myfile/CS_REVIEW/CS61C/CS61C_知识库总览.md)

## 精度声明（务必先读）

1. **HW 原题与答案不在公开网络上**：fa20 全部 11 个 Homework 都托管在 Gradescope（course 150586），只有当学期选课学生能进入。本文档提供 Gradescope 入口链接，但**不包含、也不凭记忆 reconstruct 任何 HW 题目或答案**——具体题号、分值、参数以 Gradescope 实际页面为准。
2. 本文档所有"主题 / 截止日期 / 对应 Lecture / 教材章节"均逐条核对自官方归档站课表，真实可查。
3. **公开可刷、且带官方完整答案的最佳替代品是 14 套 Discussion**（见第三部分）。Discussion 与同期 HW 由同一批教员按同一考点出题，难度和题型高度重合，是 fa20 公开资料中练习价值最高的部分，链接已全部验证有效。
4. fa20 归档站页面顶部明确标注 "this semester's archive is currently under construction, links may be broken"，个别链接（尤其考试区）可能失效。

---

## 8+1 总览卡

1. **作业总量**：11 个 Homework（Gradescope 在线完成）+ 12 个 Lab + 4 个 Project；学期 8/26 开学，12/17 期末。
2. **HW 节奏**：基本每周一个，跟随 Lecture 进度；期中前后（HW6）和期末前（HW10/11）间隔略长。
3. **知识主线**：数制 → C → 浮点 → RISC-V → 数字逻辑 → 单周期 CPU → 流水线（不单独设 HW，考试考）→ Cache → 虚存/OS/I/O → 并行 → ECC/RAID。
4. **HW1–HW4 是软件段**：位级表示、C 指针内存、IEEE 754、RISC-V 汇编与调用约定——也是失分最密集的部分。
5. **HW5–HW6 是硬件段门槛**：逻辑/FSM 与时序、单周期数据通路与控制信号，要求把一条指令在电路上走通。
6. **HW7–HW9 是存储层次段**：Cache 地址划分与 AMAT、页表/TLB、OS 与 I/O；以计算题为主。
7. **HW10–HW11 是系统与收尾段**：SIMD/TLP/MapReduce 性能编程、依赖可靠性（parity/ECC/RAID）大综合。
8. **正确的刷题姿势**：先看对应 Lecture slides → 做配套 Discussion（对官方答案）→ 再做 Lab 动手 → 最后才碰 Gradescope 上的 HW；用 P&H 教材章节查漏。

**一句话**：fa20 的 HW 题本身拿不到，但 14 套带官方答案的 Discussion 覆盖了 HW 的全部考点，按本文档的映射表逐套刷，等价于完成了作业级训练。

---

## 一、11 个 Homework 总表（信息核对自官方课表）

| HW | 主题 | 截止日(2020) | Gradescope | 对应 Lecture | 教材章节 |
|---|---|---|---|---|---|
| 1 | Number Rep 数制表示 | 9/2（W1 布置） | [605051](https://www.gradescope.com/courses/150586/assignments/605051) | Lec 1–2 | P&H 2.4 |
| 2 | C Concepts | 9/11 | [605054](https://www.gradescope.com/courses/150586/assignments/605054) | Lec 3–5 | K&R 1–8.7 |
| 3 | Floating Point 浮点 | 9/21 | [605053](https://www.gradescope.com/courses/150586/assignments/605053) | Lec 6 | P&H 3.5, 3.9 |
| 4 | RISC-V | 9/30 | [605058](https://www.gradescope.com/courses/150586/assignments/605058) | Lec 7–13 | P&H 2.1–2.12 |
| 5 | Logic, Timing 逻辑与时序 | 10/9 | [605061](https://www.gradescope.com/courses/150586/assignments/605061) | Lec 14–16 | P&H A.2–A.6 |
| 6 | RISC-V Datapath 数据通路 | 10/21 | [605063](https://www.gradescope.com/courses/150586/assignments/605063) | Lec 17–20 | P&H 4.1–4.5 |
| 7 | Caches | 11/9 | [605064](https://www.gradescope.com/courses/150586/assignments/605064) | Lec 24–27 | P&H 5.1–5.4, 5.8–5.9, 5.13 |
| 8 | Virtual Memory 虚存 | 11/9 | [605071](https://www.gradescope.com/courses/150586/assignments/605071) | Lec 28–30 | P&H 5.7–5.8 |
| 9 | OS and I/O | 11/16 | [605067](https://www.gradescope.com/courses/150586/assignments/605067) | Lec 28, 31 | P&H 5.2, 5.5, 5.11 |
| 10 | Performance Programming / Dependability | 11/24 | [605072](https://www.gradescope.com/courses/150586/assignments/605072) | Lec 32–38 | P&H 1.7–1.8, 6.1–6.7 |
| 11 | ECC, Parity & Potpourri 大综合 | 12/2 | [605073](https://www.gradescope.com/courses/150586/assignments/605073) | Lec 38, 40 | P&H 5.2, 5.5, 5.11 |

> 注：Lec 21–23 的 Pipelining（流水线与冒险）**没有单独 HW**，但属于考试核心，配套 Discussion 8 必须刷。

---

## 二、逐个 HW 的考点范围与公开配套练习

> 考点范围依据官方课表中该 HW 对应的 Lecture 标题与指定教材章节整理，描述的是"该作业覆盖的知识区"，不是对具体题目的还原。

### HW 1 · Number Rep（Due 9/2）
- **覆盖**：Lec 1 课程大图景（抽象、摩尔定律、并行）；Lec 2 数制表示。
- **知识范围**：二/十/十六进制互转；无符号数、二补码（Two's Complement）、偏置码（Bias）的取值范围与溢出判定；n 位能表示多少种状态；IEC 前缀（Ki/Mi/Gi…）；按位计数（地址空间需要多少位）。
- **官方 slides**：[lec02.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec02.pdf)
- **配套公开练习**：[Discussion 1 题目](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc01.pdf) / [**官方答案**](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc01_sol.pdf)
- **动手**：[Lab 0 环境搭建](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab00/)、[Lab 1 数制/C/cgdb](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab01/)

### HW 2 · C Concepts（Due 9/11）
- **覆盖**：Lec 3 C 基础、Lec 4 指针/数组/字符串、Lec 5 内存管理。
- **知识范围**：编译四阶段；指针本质与跨步；数组退化、二维数组 vs 指针数组；字符串与 `\0`；栈/堆/静态区；malloc/calloc/realloc/free 配对、悬空指针与泄漏；struct 对齐；cgdb 调试。
- **官方 slides**：[Module-2-C.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/2020Fa-CS61C-2020Fa-Module-2-C.pdf)
- **配套公开练习**：[Discussion 2 题目](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc02.pdf) / [**官方答案**](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc02_sol.pdf)
- **动手**：[Lab 2 Advanced C](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab02/)；同期 [Project 1（C）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/projects/proj1/) Due A 9/16 / B 9/19

### HW 3 · Floating Point（Due 9/21）
- **覆盖**：Lec 6 浮点（P&H 3.5, 3.9）。
- **知识范围**：IEEE 754 三字段（符号/指数/尾数）；bias 计算；规格化/非规格化/±∞/NaN 边界编码；float 能表示的整数范围；浮点比较与舍入；位级手算。
- **官方 slides**：[lec06.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec06.pdf)；[IEEE 754 可视化模拟器](https://www.h-schmidt.net/FloatConverter/IEEE754.html)
- **配套公开练习**：[Discussion 3 题目](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc03.pdf) / [**官方答案**](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc03_sol.pdf)

### HW 4 · RISC-V（Due 9/30）
- **覆盖**：Lec 7 入门 → Lec 8 lw/sw 与分支 I → Lec 9 分支 II → Lec 10 过程调用 → Lec 11–12 指令格式 I/II → Lec 13 编译/汇编/链接/加载（CALL）。
- **知识范围**：寄存器约定（zero/ra/t/a/s/sp，caller vs callee saved）；load-store 架构；条件分支与循环的汇编翻译；栈帧 prologue/epilogue 与递归走查；R/I/S/SB/U/UJ 六类指令格式与机器码编码；lui+addi 拼 32 位立即数（符号扩展进位）；CALL 全流程。
- **官方 slides**：[lec07](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec07.pdf)、[lec08](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec08.pdf)、[lec09](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec09.pdf)、[lec10](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec10.pdf)、[lec11](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec11.pdf)、[lec12](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec12.pdf)、[lec13](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec13.pdf)
- **配套公开练习**：[Discussion 4（入门/控制流/ISA）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc04.pdf) / [答案](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc04_sol.pdf)；[Discussion 5（过程调用/CALL）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc05.pdf) / [答案](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc05_sol.pdf)
- **动手**：[Lab 3 RISC-V 汇编](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab03/)、[Lab 4 函数与指针](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab04/)；同期 [Project 2（RISC-V）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/projects/proj2/) Due A 10/1 / B 10/5

### HW 5 · Logic, Timing（Due 10/9）
- **覆盖**：Lec 14 同步数字系统入门、Lec 15 状态与状态机、Lec 16 组合逻辑。
- **知识范围**：布尔代数与德摩根；门延迟与关键路径；组合逻辑无环路；时钟边沿触发的寄存器/触发器；建立保持时间；Moore/Mealy FSM 画法；Logisim 基本元件。
- **官方 slides**：[lec14](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec14.pdf)、[lec15](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec15.pdf)、[lec16](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec16.pdf)
- **配套公开练习**：[Discussion 6（SDS/逻辑/FSM）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc06.pdf) / [**官方答案**](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc06_sol.pdf)
- **动手**：[Lab 5 Logisim](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab05/)

### HW 6 · RISC-V Datapath（Due 10/21）
- **覆盖**：Lec 17 组合逻辑块（加法器/ALU/MUX/寄存器堆）、Lec 18–19 单周期数据通路 I/II、Lec 20 单周期控制。
- **知识范围**：IF/ID/EX/MEM/WB 五阶段在电路上的连接；ALU 与各 MUX 控制端；RegWrite/MemWrite/MemtoReg/ALUSrc/Branch/PCSel 等控制信号按 opcode 产生真值表；单周期关键路径（为什么周期由最慢指令决定）。
- **官方 slides**：[lec17](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec17.pdf)、[lec18](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec18.pdf)、[lec19](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec19.pdf)、[lec20](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec20.pdf)
- **配套公开练习**：[Discussion 7（单周期数据通路）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc07.pdf) / [**官方答案**](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc07_sol.pdf)
- **动手**：[Project 3（CPU）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/projects/proj3/) Due A 10/16 / B 11/1
- **紧随其后（无独立 HW、考试核心）**：Lec 21–23 流水线 I/II/III，[Discussion 8（流水线与冒险）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc08.pdf) / [答案](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc08_sol.pdf)；[Lab 6 流水线与 CPU](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab06/)

### HW 7 · Caches（Due 11/9）
- **覆盖**：Lec 24–27 Cache I–IV（P&H 5.1–5.4, 5.8–5.9, 5.13）。
- **知识范围**：局部性原理；地址位切分 tag/index/offset；直接映射/组相联/全相联的命中判定与硬件成本；缺失三 C；write-through vs write-back、write-allocate；AMAT 公式与多级 cache 嵌套；不同遍历顺序/AoS vs SoA 的 miss 分析。
- **官方 slides**：[lec24](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec24.pdf)、[lec25](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec25.pdf)、[lec26](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec26.pdf)、[lec27](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec27.pdf)；[Cache 流程图讲义](https://www-inst.eecs.berkeley.edu/~cs61c/sp21/resources-pdfs/caches.pdf)
- **配套公开练习**：[Discussion 9（Cache 与 AMAT）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc09.pdf) / [**官方答案**](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc09_sol.pdf)
- **动手**：[Lab 7 Caches](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab07/)

### HW 8 · Virtual Memory（Due 11/9）
- **覆盖**：Lec 28 OS 与虚存入门、Lec 29–30 虚存 I/II（P&H 5.7–5.8）。
- **知识范围**：虚地址 vs 物理地址；VPN/offset 切分；页表项（valid/dirty/权限位）；缺页异常与换页；多级页表为什么省空间；TLB 命中/缺失与地址翻译全过程；上下文切换。
- **官方 slides**：[lec28](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec28.pdf)、[lec29](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec29.pdf)、[lec30](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec30.pdf)
- **配套公开练习**：[Discussion 10（OS 与虚存）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc10.pdf) / [**官方答案**](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc10_sol.pdf)
- **动手**：[Lab 8 OS/上下文切换/I/O/DMA/磁盘/网络/虚存](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab08/)

### HW 9 · OS and I/O（Due 11/16）
- **覆盖**：Lec 31 I/O（P&H 5.2, 5.5, 5.11）。
- **知识范围**：轮询 vs 中断；DMA；磁盘结构与访问时间（寻道/旋转/传输）；总线与 I/O 编址；网络与存储设备的性能粗算。
- **官方 slides**：[lec31.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec31.pdf)
- **配套公开练习**：[Discussion 11（I/O）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc11.pdf) / [**官方答案**](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc11_sol.pdf)

### HW 10 · Performance Programming / Dependability（Due 11/24）
- **覆盖**：Lec 32 Flynn 分类与 SIMD、Lec 33–35 线程级并行 I–III（OpenMP）、Lec 36 MapReduce/Spark、Lec 37 数据中心与云计算、Lec 38 依赖可靠性（parity/ECC/RAID）。
- **知识范围**：Amdahl 定律；SIMD 向量化条件；OpenMP parallel for / reduction / 私有与共享 / false sharing；MPI 与消息传递概念；MapReduce 的 map-shuffle-reduce 与容错；WSC 仓储级计算；RAID 0–5 的容量与可靠性权衡（RAID 细节在 HW11 继续）。
- **官方 slides**：[lec32](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec32.pdf)、[lec33](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec33.pdf)、[lec34](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec34.pdf)、[lec35](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec35.pdf)、[lec36](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec36.pdf)、[lec37](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec37.pdf)
- **配套公开练习**：[Discussion 12（数据级并行）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc12.pdf) / [答案](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc12_sol.pdf)；[Discussion 13（一致性/原子/并行）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc13.pdf) / [答案](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc13_sol.pdf)
- **动手**：[Lab 9 SIMD](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab09/)、[Lab 10 线程级并行](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab10/)；同期 [Project 4](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/projects/proj4/) Due 12/4

### HW 11 · ECC, Parity & Potpourri（Due 12/2）
- **覆盖**：Lec 38 依赖可靠性 + 全学期大综合（potpourri）。
- **知识范围**：奇偶校验（parity）、汉明距离与纠错能力（SEC/DED）、ECC 内存；RAID 各级别综合；其余为全课程易错点回锅。
- **官方 slides**：[lec38.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/lectures/lec38.pdf)
- **配套公开练习**：[Discussion 14（WSC/RAID/Spark/MapReduce/Parity/ECC）](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc14.pdf) / [**官方答案**](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc14_sol.pdf)
- **动手**：[Lab 11 Spark/可靠性](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab11/)

---

## 三、公开题库：14 套 Discussion（题目 + 官方答案，刷题主力）

URL 规律：`https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/discXX.pdf`（题目）与 `discXX_sol.pdf`（答案）。每套含 Pre-Check 概念判断题 + 正题，答案是教员手写的完整解析。

| # | 主题（官网原标题） | 题目 | 官方答案 | 服务于 |
|---|---|---|---|---|
| 1 | Number Rep | [disc01.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc01.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc01_sol.pdf) | HW1 |
| 2 | C Basics | [disc02.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc02.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc02_sol.pdf) | HW2 |
| 3 | Floating Point | [disc03.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc03.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc03_sol.pdf) | HW3 |
| 4 | RISC-V Intro, Control Flow, ISA | [disc04.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc04.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc04_sol.pdf) | HW4 |
| 5 | RISC-V Procedures, CALL | [disc05.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc05.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc05_sol.pdf) | HW4 |
| 6 | SDS, Logic, FSM | [disc06.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc06.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc06_sol.pdf) | HW5 |
| 7 | Single-Cycle Datapath | [disc07.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc07.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc07_sol.pdf) | HW6 |
| 8 | Pipelining and Hazards | [disc08.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc08.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc08_sol.pdf) | 无 HW，考试核心 |
| 9 | Caches & AMAT | [disc09.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc09.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc09_sol.pdf) | HW7 |
| 10 | OS & Virtual Memory | [disc10.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc10.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc10_sol.pdf) | HW8 |
| 11 | I/O | [disc11.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc11.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc11_sol.pdf) | HW9 |
| 12 | Data-level Parallelism | [disc12.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc12.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc12_sol.pdf) | HW10 |
| 13 | Coherency and Atomic, Parallelism | [disc13.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc13.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc13_sol.pdf) | HW10 |
| 14 | WSC, RAID, Spark, MapReduce, Parity & ECC | [disc14.pdf](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc14.pdf) | [sol](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/disc14_sol.pdf) | HW11 |

> 另有每节 Discussion 的官方讲解视频（YouTube 播放列表），链接在归档课表对应周次内，适合做题卡壳时跟听。

---

## 四、Lab 与 Project 索引（页面全部公开）

### Labs（URL 规律：`/fa20/labs/labNN/`）

| Lab | 主题 |
|---|---|
| [Lab 0](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab00/) | Intro and Set Up |
| [Lab 1](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab01/) | Number Rep, C and CGDB |
| [Lab 2](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab02/) | Advanced C |
| [Lab 3](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab03/) | RISC-V Assembly |
| [Lab 4](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab04/) | RISC-V Functions, Pointers |
| [Lab 5](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab05/) | Logisim |
| [Lab 6](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab06/) | Pipelining and CPU |
| [Lab 7](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab07/) | Caches |
| [Lab 8](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab08/) | OS (context switch), I/O, DMA, Disks, Networking & VM |
| [Lab 9](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab09/) | SIMD Instructions |
| [Lab 10](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab10/) | Thread Level Parallelism |
| [Lab 11](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/labs/lab11/) | Spark / Dependability |

### Projects（两阶段截止，页面公开）

| Project | 内容方向 | Due A / Due B (2020) |
|---|---|---|
| [Project 1](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/projects/proj1/) | C 编程（指针/内存/字符串综合） | 9/16 / 9/19 |
| [Project 2](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/projects/proj2/) | RISC-V 汇编 | 10/1 / 10/5 |
| [Project 3](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/projects/proj3/) | Logisim CPU（单周期 → 流水线） | 10/16 / 11/1 |
| [Project 4](https://www-inst.eecs.berkeley.edu/~cs61c/fa20/projects/proj4/) | 性能优化竞赛 | 12/4 |

---

## 五、考试信息与 fa20 全套真题（公开，含官方答案）

- **Final**：2020/12/17，线上全天窗口，3 个 Section、总计 3 小时。
- 期末复习官方资料（链接自归档课表第 16 周）：
  - [Conceptual Review Slides](https://docs.google.com/presentation/d/1yDwTpiwpwtAMO-lsJ9U6ctOfwbVDTWHawLcCADNrXoM/edit?usp=sharing)
  - [Review Worksheet](https://docs.google.com/document/d/1KcajGkGebZbdxJniva5t2MRNBYwB8Xc6QIeSy_43Ng4/edit?usp=sharing)
  - [Exam Question Review 用卷 PDF](https://drive.google.com/file/d/1hAcWNFdIVjuBJ7ihUqcxZecGZZHuxbS9/view?usp=sharing)

### fa20 三套真题 + 官方答案（GitHub 公开备份，2026-10 验证可下）

仓库：[iwantsomememories/CS61C_FA20](https://github.com/iwantsomememories/CS61C_FA20)（学生整理的 fa20 全套资料：labs / projects / discussions / handouts / lectures / **exams**；注意该仓库同样没有 HW——Gradescope 作业学生无法导出）。

| 试卷 | 空白卷 | 官方答案 |
|---|---|---|
| Quest（第 5 周小测，覆盖数制/C/浮点/RISC-V 入门） | [Fa20_Quest_Blank.pdf](https://raw.githubusercontent.com/iwantsomememories/CS61C_FA20/master/exams/Fa20_Quest_Blank.pdf) | [Solutions](https://raw.githubusercontent.com/iwantsomememories/CS61C_FA20/master/exams/Fa20_Quest_Solutions.pdf) / [Solutions 2](https://raw.githubusercontent.com/iwantsomememories/CS61C_FA20/master/exams/Fa20_Quest_Solutions2.pdf) |
| Midterm（第 8 周左右，考到数据通路） | [Fa20_Midterm_Blank.pdf](https://raw.githubusercontent.com/iwantsomememories/CS61C_FA20/master/exams/Fa20_Midterm_Blank.pdf) | [Solutions](https://raw.githubusercontent.com/iwantsomememories/CS61C_FA20/master/exams/Fa20_Midterm_Solutions.pdf) / [重排版 Solutions](https://raw.githubusercontent.com/iwantsomememories/CS61C_FA20/master/exams/Fa20_Midterm_Solutions-rewritten.pdf) |
| Final（全课程综合） | [Fa20_Final_Blank.pdf](https://raw.githubusercontent.com/iwantsomememories/CS61C_FA20/master/exams/Fa20_Final_Blank.pdf) | [Solutions](https://raw.githubusercontent.com/iwantsomememories/CS61C_FA20/master/exams/Fa20_Final_Solutions.pdf) |

> 若 raw 直链打不开，用仓库目录页进入：[exams/](https://github.com/iwantsomememories/CS61C_FA20/tree/master/exams)。
> 真题的用法：先按考试时间限时做 Blank 卷，再对 Solutions；错题回到对应的 Discussion 专题重刷。真题综合性强于 Discussion，建议放在每段学习之后而不是之前。

---

## 六、建议的六周刷题路线（用公开材料替代拿不到的 HW）

1. **第 1 段·位与 C（HW1–2 区）**：Disc1 → Disc2，每道位级转换手算到底；同步 Lab 1–2，C 代码全部过 valgrind/cgdb。
2. **第 2 段·浮点与汇编（HW3–4 区）**：Disc3 配合 IEEE 754 模拟器；Disc4、Disc5 连刷，重点是递归汇编走查和指令编码；Lab 3–4 在 Venus 里跑通。
3. **第 3 段·逻辑与 CPU（HW5–6 区）**：Disc6 → Disc7，控制信号自己列真值表；Disc8（流水线）单独刷透，画阶段时间轴；Lab 5–6 在 Logisim 里复现。
4. **第 4 段·存储（HW7–9 区）**：Disc9–11，cache 地址划分和 AMAT 做到秒算；VM 题画 VPN→PPN 全流程。
5. **第 5 段·并行与可靠性（HW10–11 区）**：Disc12–14，Amdahl 定律、false sharing、RAID 容量/可靠性表格化整理；Lab 9–11 动手。
6. **冲刺**：用第 16 周 Review Worksheet + 历年真题限时 3 小时模拟。

---

## 七、跨学期调查：为什么"往后找"也拿不到在线 HW（2026-10 实测）

按 fa20 → sp26 顺序逐学期核实，在线作业平台全部在校方认证之后，且呈"越来越封闭"的趋势：

| 学期 | HW 平台 | 免登录访问 | 备注 |
|---|---|---|---|
| fa20、sp21 | Gradescope | 否（CalNet） | 本文档目标学期 |
| fa21、sp22 | cbt-dev.berkeley.edu（伯克利自建 PrairieLearn） | 否（CalNet） | sp22 共 11 个 HW，主题与 fa20 高度一致 |
| sp26（最新） | us.prairielearn.com（PL 官方云） | 否（Berkeley SSO + 选课名单） | 10 个 HW |

旁证：GitHub 上学生备份的 fa20 全资料仓库收录了 labs/projects/discussions/exams/handouts/lectures，**唯独没有 HW 目录**——计分作业在 Gradescope 内完成，学生本地也没有题目副本。这是课程组的刻意设计（题目随机化、重复使用），不是链接失效。

**但同学期的练习材料全部公开**，已实测可下：

1. **fa20 Discussion 14 套 + 官方答案**：见第三部分，`www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/`。
2. **sp22 Discussion 13 套 + 官方答案**：题目与 fa20 同源（实测 disc01 与 fa20 几乎逐字相同，题库稳定），可作二刷变式。URL 规律 `https://www-inst.eecs.berkeley.edu/~cs61c/sp22/pdfs/discussions/discXX.pdf` 与 `discXX-sols.pdf`（注意 sp22 命名带 s：`-sols`）；索引页 `https://www-inst.eecs.berkeley.edu/~cs61c/sp22/discussions/discNN/`。
3. **fa20 Quest / Midterm / Final 真题 + 官方答案**：见第五部分 GitHub 直链。
4. **fa20 Labs / Projects 全部页面与 skeleton**：见第四部分及 GitHub 仓库。
5. PrairieLearn（us.prairielearn.com）支持任意邮箱免费注册，官方有公开示范课程与题库（PL Example Course）可刷同类型的数制/浮点/cache 题，但无法进入伯克利 course_instance 205444 计学分。

---

## 来源

- 课程归档（课表 / 截止日 / Lecture 标题 / P&H 章节 / Discussion 链接）：https://www-inst.eecs.berkeley.edu/~cs61c/fa20/
- HW 入口（需当学期 Gradescope 权限）：https://www.gradescope.com/courses/150586
- Discussion 题目与官方答案：`https://www-inst.eecs.berkeley.edu/~cs61c/fa20/pdfs/discussions/`（2026-10 验证链接有效）
- 概念详解配套：[CS61C_知识库总览.md](file:///d:/myfile/CS_REVIEW/CS61C/CS61C_知识库总览.md)
