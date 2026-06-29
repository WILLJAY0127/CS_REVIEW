---
lecture: 4
title: Higher-Order Functions
week: 2
textbook: "Ch.1.6"
homework: "HW02"
status: complete
---

# Lecture 4 · Higher-Order Functions —— 抽象能走多远

> **这节课回答的总问题**:如果函数本身可以像数字一样被传进、传出,抽象的力量能走多远?
>
> 核心思想:当计算过程本身也能像值一样被传来传去时,抽象能走多远、又能解决什么接口约束问题。

## 配套资源

- 视频:YouTube playlist,起始 ID `pveIuZT0GJE`,list `PL6BsET-8jgYXvcnnEX7x2_USaYug9xZFv`
- 教材:Composing Programs Ch.1.6(Higher-Order Functions)
- 幻灯片:`04-Higher-Order_Functions.pdf`
- 作业:**HW02: Higher-Order Functions**(product / accumulate / make_repeater)
- 相关:Disc 01(Control, Environment Diagrams);Lab 02(HOF, Lambda Expressions)

**关于 Lambda / Currying 的归属判断**(对话末尾):
- Jace 明确指出:"Lambda 表达式 / Currying 柯里化 这俩个我在视频里还没有看到啊"
- Claude 核对课程表后确认:Lecture 4 和 Lecture 5 **都对应 Ch.1.6**,Ch.1.6 被拆分到两讲;Lambda、Currying(教材 1.6.6、1.6.7)大概率属于 **Lecture 5 · Environments**,需在 L5 的 C 阶段确认覆盖范围并补进笔记
- 续接设定中已记为"待办"——**已由 [[05 - Environments]] 落实**

## 知识脉络(分层推进 + 层间桥梁)

```
调用表达式急切求值 / 控制语句惰性求值 → 不可替代
→ 函数可接受函数作参数(抽象计算规则,消除结构重复)
→ 函数可返回函数(闭包封存上下文,满足接口约束保留私有状态)
→ 函数是一等公民(关注点分离,组合构建复杂行为)
```

### 第一层:求值规则的裂缝

- Fibonacci 的 while 实现(`pred`/`curr`/`k`/`n` 四个状态变量)作为开场,提示多变量迭代是高频模式,将被抽象;含第 0 项边界优化
- **挑衅问题**:能否用普通函数替代 if/else?`if_(condition, a, b)` 技术可行,但**调用表达式先把所有参数算出来再调用**,导致 `if_(x>0, sqrt(x), 0)` 在 x 为负时 `sqrt(x)` 已被执行并报错
- `and`/`or` 是**控制表达式**,有**短路求值**:`x>0 and sqrt(x)>10` 左假则右不执行;`n==0 or 1/n!=0` 左真则右不触发
- **本层结论**:函数(调用表达式)急切求值所有参数;控制语句与短路运算符按条件决定是否求值。两者求值纪律根本不同,不可互相替代

> **桥 1→2**:函数替代不了控制语句,这是函数的边界。但在函数本身的能力上还有另一片天地没探索——既然函数是一个值,它能不能作为参数传给另一个函数?

### 第二层:函数作为参数 —— 抽象"变化的计算"(→ Strategy Pattern)

- **面积例子**:正方形/圆形/正六边形公式骨架相同(`系数 × 边长²`),只有系数不同
- **数列求和**更彻底:`sum_naturals`/`sum_cubes`/`pi_sum` 循环骨架一模一样,只有"每一项怎么算"不同。把变化的计算提取成参数 `term`(一个函数)。`summation(n, term)` 传 `cube` 算三次方,传 `identity` 算自然数
- **关键认知**:不是消除重复的数字,而是消除重复的**计算结构**;"如何把 k 变成一项"是一种规则,规则可成为参数
- **HOF 定义**:接受函数作为参数、或返回函数作为结果

> **桥 2→3**:传入函数解决了"同一骨架、不同计算"。但有时面对的是另一类约束——通用框架(如 `improve` 迭代改进算法)只接受特定签名的函数,而具体计算天然需要更多上下文。直接加参数行不通,需要返回函数。

### 第三层:函数作为返回值 —— 用闭包封存上下文(→ Decorator Pattern)

- `improve(update, close, guess=1)` 框架求平方根,期望 `update` 是只接受当前猜测 `x` 的单参数函数;但更新规则天然需要 `x` 和目标 `a` 两个量
- **解法**:在 `sqrt(a)` 内部定义 `sqrt_update(x)`,只暴露 `x`,让 `a` 从父帧自动捕获
- **直接连接 [[03 - Control]]**:函数对象存三样东西——形参列表、冷冻函数体、**父帧地址**。`sqrt_update` 在 `sqrt` 帧内定义,父帧地址指向 `sqrt` 帧
- `sqrt_update` 被返回传给 `improve` 后,`sqrt` 调用结束——但 `sqrt` 帧**不消失**,因为 `sqrt_update` 还持有指向它的父帧地址。`improve` 后续调用 `sqrt_update(x)` 时,新帧找不到 `a`,沿父帧链向上找到 `sqrt` 帧里的 `a`
- 环境图里复杂的"调用树":每个函数对象有向上的箭头(父帧地址),名称解析沿箭头往上爬。**与 Lecture 3 规则完全一致,没有新规则,只是链条更长**
- **闭包定义**:函数对象携带它被定义时的环境(通过父帧地址),即使被返回到别处执行,仍能看到那个环境的绑定。闭包不是新机制——是父帧地址在更复杂场景下的自然延伸
- **回答"为什么不直接加参数"**:不是不行,而是不总有这个权利。`improve` 是通用框架,接口规定 `update` 必须单参数。没法改 `improve`,但可用闭包把 `a` 藏进 `sqrt_update`,对外只暴露 `x`。返回函数的本质 = **在满足接口约束的同时,把此刻的上下文永久锁进函数对象**

> **桥 3→4**:函数可传入、可传出、可在内部创建、可携带环境游走——这意味着函数和数字一样是彻底的"值"。还有两个实用语法对应这个结论。

### 第四层:语法收尾 —— Lambda、装饰器与一等公民

- **Lambda**:匿名函数简写,只单个返回表达式,无赋值、无复杂控制流(需条件用三元 `x if x>0 else -x`)
- **Currying**:把多参数函数转成一系列单参数函数链条;`curry2(pow)` 可"固定"首参得到专用单参函数
- **装饰器**:HOF 的语法糖;`@trace` 写在 `def triple` 上方,等价于 def 执行后立即 `triple = trace(triple)`,不改原函数包上额外行为
- **一等公民**:函数可绑定名字、作参数、作返回值、放进数据结构,与整数字符串完全平等。后果:每个函数只做一件事,复杂行为靠组合实现(关注点分离)

## 我的理解(费曼推导链,保留原话)

> 最开始我以为函数里装的是"逻辑和绑定",但推导之后发现说得不够准确。函数对象在被调用之前,形参没有值。它真正存的是三样东西:形参列表、冻结的逻辑、还有**定义它时所在帧的地址**。注意是定义时,不是调用时——同一个函数被两个不同的地方调用,它找名字永远回到它出生的那个帧,而不是调用它的帧。
>
> 名字求值这件事也比我以为的简单:对一个名字求值,就是去当前帧找它绑定的值,得到的就是那个值对应的对象。如果 `cube` 绑定的是一个函数对象,那对 `cube` 求值就得到那个函数对象本身,不会调用它。所以 `summation(3, cube)` 里,`cube` 被求值后变成函数对象,作为值绑定进 `summation` 的帧里,和整数 3 完全平等。这就是"函数是一等公民"最具体的含义。
>
> `cube` 在 global frame 里被 def 出来,所以它的父帧就是 global frame。`summation` 内部调用 `term(k)` 时,新建的 `cube` 帧向上找名字,找的是 global frame,不是 `summation` 的帧。
>
> 闭包机制也是这条规则的延伸:`make_adder(3)` 执行时,内部创建了 `adder` 函数对象,父帧地址指向 `make_adder` 的帧(`n=3` 在那里)。`make_adder` 返回后,帧理论上应该消失,但因为 `adder` 还拿着指向那个帧的地址,帧就不能被销毁。**闭包 = 函数对象 + 它出生时捕获的环境帧。** 函数带着这个环境到处走,随时能找到里面的绑定。
>
> "为什么要返回函数"困惑了我很久。后来想通了:传出函数不是目的,是为了造出一个"预先藏好了上下文"的函数,再传给框架用。`improve` 只接受单参数函数,但 `sqrt_update` 需要知道 `a`。在 global frame 写 `sqrt_update` 它不知道 `a` 是什么,所以必须在 `sqrt(a)` 内部创建它,让它捕获 `a`,再返回出去传给 `improve`。**传出是手段,传入才是目的。**
>
> 用 Java 的语言说:函数作为参数是 Strategy Pattern,`improve(update, close)` 和 `Collections.sort(list, comparator)` 是同一个思路。函数作为返回值是 Decorator Pattern,`@trace` 和 `BufferedInputStream` 包 `FileInputStream` 是同一个思路。Java 实现这两个模式需要接口和类;Python 因为函数是一等公民,一个函数就够了。
>
> 最后一点:函数和控制语句不可互相替代,因为求值纪律根本不同。函数会先把所有参数都算出来,没有办法跳过某段计算;`if/else` 和短路运算符才能做到按条件决定执行哪段代码。

**推导过程的关键原话节点**(费曼对话中 Jace 逐步推出来的):

| 阶段 | 提问 | Jace 的回答 |
|---|---|---|
| 起步 | 函数里装着什么? | "逻辑和绑定" → 被追问形参 → "就记住了逻辑" → 被点 `def square(x)` 的 x → "哦哦 入参 出参 还有逻辑" |
| **父帧关键突破** | 还有什么? | 先答"还有调用他的帧的地址?" → 反问"谁叫这个函数,它就去谁那里找名字吗?" → "我不知道" → 用 A定义/B调用 场景 → "肯定去 A 啊" → 被指出矛盾 → **"记住的是定义它的 A"** ✓ |
| **帧存活突破** | 外层帧还在吗? | 先答"不在了啊" → 钥匙/箱子类比反问 → **"不能的,如果函数被关联上了,对应的上下文全部都保留?那这个帧就一直存在是么"** ✓ |
| 闭包定义 | 返回的函数携带什么? | "携带了完整的闭包,但我不知道闭包怎么形容" → 被引导合成 → **"携带了当前的函数对象加上他的环境帧"** ✓ |
| **返回函数动机突破** | 传出函数有什么用? | 长时间困惑"如果传入函数能解决,那还需要传出函数做什么??" → 想通后 → **"传出是手段,传入才是目的"** |
| 求值规则突破 | 为何 if_ 封装会出问题? | "因为函数会先求值参数里的表达式" → if/else"不会,他会控制" → **"不能,那就是编程语言需要实现这种控制代码执行的逻辑"** |
| 名字求值突破 | `summation(3, cube)` 对 cube 求值得到什么? | **"求值得到对应的对象?"** ✓ |

## Java / 设计模式桥梁(本讲重点)

### 桥梁一:函数作为参数 = Strategy Pattern

```java
Collections.sort(list, (a, b) -> a.compareTo(b));  // Java
```
```python
summation(n, term)       # term 就是'策略'
improve(update, close)   # update 和 close 都是策略
```

> 把"变化的行为"提取成参数传进来,框架保持不变。一模一样。

Jace 确认后:"传入函数 → Strategy Pattern / 传出函数 → Decorator Pattern……这节课的两个核心操作,你在 Java 里全用过,只是换了形式"

### 桥梁二:函数作为返回值 = Decorator Pattern

```java
InputStream in = new BufferedInputStream(new FileInputStream(file));  // 包一层,加缓冲
```
```python
@trace
def triple(x):
    return 3 * x   # 包一层,加打印
```

> **Python 的 `@decorator` 语法之所以叫"装饰器",就是因为它就是 Decorator Pattern。** `trace(triple)` 接收一个函数,返回一个增强版的函数——和 `BufferedInputStream` 包 `FileInputStream` 是同一个思路。

### 桥梁三(核心突破):一等公民让两种模式比 Java 的类实现轻得多

Jace 的啊哈原话:
> **"有点懂了,所以我可以理解 java 里实现起来比较复杂的装饰器,一般是类的组合,在 py 里用一等公民函数就搞定了对么"**

Claude 肯定并展开:
> "对,你说到点上了。Java 实现装饰器要写接口、抽象类、具体类——一堆样板代码,只是为了'包一层行为'。Python 因为函数是一等公民,直接一个函数接收函数、返回函数,不需要任何类。**这就是'函数是一等公民'的实际价值**。"

### 桥梁四:Java lambda 捕获 = Python 闭包

```java
double a = 256;
improve(x -> average(x, a/x), ...)  // lambda 捕获了 a
```

> 你在 Java 里写 lambda 时,lambda 也在"捕获"外部变量。`make_adder` 做的是完全一样的事——只是 Python 用 `def` + `return` 来表达。传出函数 = 造一个捕获了上下文的函数,为了传进去用。

### 桥梁五:improve = Template Method Pattern(提及未深入)

> `improve` defines the skeleton of iteration until convergence, letting you inject the specific update and close logic. This is essentially the same structure as a Java abstract class with template methods, just expressed through higher-order functions instead of inheritance.

**"求值顺序是函数和控制语句不能互相替代的根本原因"** —— 与设计模式桥梁并列为本讲两大认知突破。

## HW02 答题过程(苏格拉底式,记录推导与纠错)

### Q1: product

- Claude 问"`summation` 是把每一项**加**起来。`product` 需要做什么?"
- Jace 直接写出代码(含语法错误:`def product(n,term)` 漏冒号)
- **纠错1(语法)**:漏冒号 `:`,需补上
- **纠错2(执行方式)**:"跑完了没有结果" → 改成 `print(product(3, identity))` 才输出(脚本无 print 不输出)。`square` 需自己定义(非内置),结果 36 ✓
- **关键反思**:问"和 `summation` 比改了哪两个地方?" → 只答出"改成了 * 法"。追问初始值——`summation` 是 `total=0`,`product` 是多少、为什么不能用 0?→ **"0*任何都是0"**
- **结论**:两处不同——初始值 `0`→`1`(乘法单位元),操作 `+`→`*`;骨架完全一样。这就是 HOF 价值:`summation` 与 `product` 共享结构,只这两点不同

### Q2: accumulate

- 问"你 `product` 里有两个硬编码的东西——初始值和操作。`accumulate` 的参数里哪两个对应?" → "累加或者乘 以及 初始值" → 即 `fuse` 和 `start`
- **第一版(有 bug)**:
  ```python
  def accmolate(fuse,start,n, term):
      t = start        # 错:把 start 当循环计数器
      total = 1        # 错:total 初值硬编码成 1,应为 start
      while t <= n:
          total = fuse(total , term(t))
          t = t + 1
      return total
  ```
- **纠错路径**:让先跑 `print(accumulate(add, 11, 5, identity))`(期望 26)。Jace"结果是 1"。让回头看 `product` 里 `t` 和 `total` 各自什么作用——**这是 loop counter 和 accumulator 初值混淆的根因**:`product` 里 `t` 和 `total` 恰好都是 1,导致 Jace 把两者混为一谈;`accumulate` 里 `t` 仍应从 1 起、`total` 应从 `start` 起
- **Jace 自纠第二版**:`t = 1; total = start`。验证 `accumulate(add,11,5,identity)`=26、`accumulate(mul,2,3,square)`=72 ✓
- **一行版**:`summation_using_accumulate` → `return accumulate(add, 0, n, term)`;`product_using_accumulate` → `return accumulate(mul, 1, n, term)`
- **结论**:`summation` 和 `product` 现在都只是 `accumulate` 的一行调用,`fuse` 和 `start` 是唯一区别

### Q3: make_repeater

- 问"`make_repeater(f, n)` 需要返回什么?" → "返回 f(f()) 总共 n 次这样一个方法"
- 问"内层函数里怎么把 `f` 连续应用 `n` 次?" → **"不知道 完全不会"**
- 拆解:用具体例 `square(square(5))`,给起步 `result=5`,让填两步 → "25 和 25 的平方"(即 25、625)
- 提炼模式:每一步 `result = f(result)`,重复 n 次,用 while
- **第一版(有 bug)**:
  ```python
  def make_repeater(f, n):
      def repeater(x):
          count = 0
          total           # 错:未赋值
          while count < n:
              total = f(x)   # 错:每次都用原始 x,没有反馈
              count = count + 1
          return total
      return repeater
  ```
- **纠错路径**:问"在你的循环里,每次都是 `f(x)`——`x` 的值会变吗?第二次循环时,`f(x)` 算的是什么?"——**这是 `f(x)` 误用为 `f(total)` 的根因**:Jace 没把上一步结果反馈进下一步
- **Jace 自纠第二版**:`total = x; while count < n: total = f(total)`。验证 `make_repeater(square, 3)(5)`=390625 ✓

> 三题收尾(Claude):"回头看这三题:`product` → `accumulate` → `make_repeater`,每一道都是 HOF——要么传入函数,要么返回函数,要么两个都有。"

## 关键纠错与突破

**Claude 主动纠正**:
1. **父帧地址 = "定义它的帧",不是"调用它的帧"**(最关键纠错)。Jace 先答"还有调用他的帧的地址?",Claude 反问"谁叫这个函数,它就去谁那里找名字吗?"并给 A定义/B调用 场景,Jace 自己改口"记住的是定义它的 A"。这区分了**词法作用域 vs 动态作用域**
2. **外层帧不会随 return 消失**。Jace 先答"不在了啊",用"钥匙/箱子"类比反问,推出"如果函数被关联上了,对应的上下文全部都保留?那这个帧就一直存在是么"
3. **例子用错**:Jace 指出"为什么你总是再说 improve,实际上视频里给的例子是 make_adder 函数以及内部的 adder(k)" → 改用 `make_adder`/`adder` 这个视频里真实出现的更简单例子
4. **`cube` 的父帧指向 global,不是 summation 的帧、不是调用者帧**
5. **HW02 accumulate 的 loop counter vs accumulator 初值混淆**:`t=start` 错、`total=1` 错;正确是 `t=1, total=start`
6. **HW02 make_repeater 的 `f(x)` 应为 `f(total)`**:没有把上一步结果反馈进去
7. **product 的 `def` 漏冒号**;脚本运行需 `print()` 才有输出;`square` 需自定义而非 import

**Jace 的啊哈时刻**:
1. **"有点懂了,所以我可以理解 java 里实现起来比较复杂的装饰器,一般是类的组合,在 py 里用一等公民函数就搞定了对么"** ← 本讲最大突破,把闭包/HOF 连到 Java Decorator Pattern
2. **"传出是手段,传入才是目的"** ← 长期困惑的化解
3. **"不能,那就是编程语言需要实现这种控制代码执行的逻辑"** ← 函数急切求值 vs 控制语句惰性求值,二者不可替代
4. **"闭包 = 函数对象 + 它出生时捕获的环境帧"** ← 闭包定义合成
5. **"0*任何都是0"** ← product 初始值为何不能是 0 的瞬间顿悟

## 相关概念

- [[03 - Control]] — 前置:函数对象存三样东西(形参表+函数体+父帧地址),本讲是父帧地址在更复杂场景下的延伸
- [[05 - Environments]] — 把环境模型正式化成画图规则,机械追踪闭包;并落实 Lambda、Currying(L4 留的待办)
- [[02 - Functions]] — 一等公民概念的起点
