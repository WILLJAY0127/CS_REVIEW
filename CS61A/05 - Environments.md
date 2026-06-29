---
lecture: 5
title: Environments
week: 3
textbook: "Ch.1.6 (1.6.5-1.6.7)"
lab: "Lab 02"
status: "L+I 完成, P(Lab02) 待补"
---

# Lecture 5 · Environments —— 不靠直觉,机械地追踪函数传递

> **这节课回答的总问题**:上一课(高阶函数)让你接受了一个事实:函数可以被当参数传,也可以被当返回值返回。但这立刻带来一个新麻烦——一旦函数能被到处传来传去,光靠从上到下念代码,已经没法准确预测程序到底会发生什么了。尤其是闭包,直觉很容易猜错。这节课要解决的就是:有没有一套不依赖直觉、机械地、每次都能算对的方法,来追踪任何一段涉及函数传递的代码?
>
> 答案一句话:**把环境模型(frame)正式化成一套精确的画图规则。**

## 配套资源

- 视频:`https://www.youtube.com/watch?v=1P2UgdAWwYg`
- PDF slides:`05-Environments_1pp.pdf`(insideempire archive)
- Lab 02:`lab/lab02/index.html`
- 教材:Ch.1.6(续)——重点是 1.6.6 Currying + 1.6.7 Lambda Expressions,加贯穿全节的环境图形式化规则(Lecture 4 已消化 1.6.1–1.6.4,Lecture 5 是收尾)
- **注意**:currying 不在 lecture 正式 topic 里,是 Lab 02 练习内容(对应教材 1.6.5),Claude 提议"等看完这节课我们可以单独补一轮"

## 编号争议的结论

Jace 一度想叫 Lecture 4(因为 Welcome 讲没啥用,实际这个就是第 4 讲)。Claude 反驳,最终 Jace 接受 **Lecture 5**,论证依据:
- insideempire archive 官方页面自己写的就是 "Lecture 5: Environments"(URL 是 lecture-5-environments,slides 文件名 05-Environments_1pp.pdf)
- 与 Jace 已有笔记(Lecture 3 Control / Lecture 4 HOF)完全对得上
- 若现在重排,之后每一课编号都会跟网站官方编号、视频标题、slides 文件名对不上,且与已有笔记产生编号体系不一致

> Jace 原话:"不要叫 5,因为 1 是 welcome 没啥用,实际这个就是 4" → 接受:"好吧 那就 5"

**结论**:用官方编号,不要中途重排。

## Consume 阶段引导问题(三个核心)

1. **Slides 给出了画环境图的两条规则**——一条是"函数被定义时"做什么,一条是"函数被调用时"做什么。这两条规则分别对应你之前理解的"key"和"box"中的哪一个动作?
2. **bear/oski 陷阱**:`bear = -1`,然后 `oski = lambda print: print(bear)`,然后 `bear = -2`,最后调用 `oski(abs)`。猜猜看会打印什么——这背后说明 Python 的闭包到底是"记住了 bear 当时的值",还是"记住了能找到 bear 的那个 frame"?(跟 Java lambda 要求 "effectively final" 变量直接相关)
3. **Lambda 的环境身份**:Lambda 创建的函数,在环境图里标注的名字是什么(不是你赋给它的变量名)?这说明 lambda 和 def 之间,在"函数对象本身"这个层面上少了什么东西?

## 知识脉络(分层推进 + 层间桥梁)

### 层 1:画环境图的两条规则(定义时 / 调用时)

- **定义时**:创建函数对象,标注 parent 为当前 frame;把函数对象绑定到名字(lambda 这一步无名字可绑)
- **调用时**:新建局部 frame(标题写函数名);把函数的 parent(定义时记下的)复制到新 frame;绑定形参到实参;在新 frame 开始的环境里执行函数体
- **比喻**:"拿钥匙"(定义时 parent 定死,永不改变) vs "开箱子"(调用时新开 frame,但箱子的门锁用的是定义时那把钥匙,与谁调用、在哪调用无关)

> **桥 1→2**:这两条规则正是用来解释 Jace 一开始觉得奇怪的 apply_twice 现象。

### 层 2:apply_twice 验证——parent 只认定义,不认调用(词法作用域)

- apply_twice 内部调用的 square,其 parent 还是 Global 而不是 apply_twice 的 frame
- **原因**:square 的 parent 在 def 那一刻定死(全局定义 → Global),调用时新 frame 的 parent 抄的是 square 自己的 parent 标签,不是调用方 frame
- **反向验证**:若 square 函数体引用只在 apply_twice 局部才有的名字 → 找不到,报错
- 这套规则叫**词法作用域**(lexical scoping):谁能看见谁,写代码时就定死,与运行时调用栈无关

> **桥 2→3**:同一规则反过来用——若想让内层函数"记住"外层局部变量,必须让它的 parent 链接到外层那次调用的局部 frame,这就需要嵌套定义。

### 层 3:嵌套定义 → 闭包:为什么要把函数定义在函数里面

- **make_adder**:内层 adder 的 parent 是 make_adder 这次调用产生的局部 frame(含 n=3),所以 three_more_than(4) 能沿 parent 链查到 n=3 算出 7
- **不嵌套的反例**:两个函数都定义在 Global → 内层 parent=Global;外层局部 frame 在 return 后销毁 → 内层压根没机会"记住" n
- **结论**:嵌套定义(或 lambda)不是风格偏好,而是**闭包成立的必要条件**——不嵌套,parent 链接不上那个局部 frame

> **桥 3→4**:闭包"记住"的到底是什么?是值快照,还是 frame 引用?用 bear/oski 陷阱来证伪。

### 层 4:闭包的陷阱(bear/oski)——记住的是 frame,不是值

- 代码:`bear=-1` → `oski=lambda print: print(bear)` → `bear=-2` → `oski(abs)`
- **直觉错**:以为 oski 定义时 bear=-1,该记住 -1
- **实际**:闭包记住的是一条能查到 bear 的 frame 路径,调用时才查,此时 Global 里 bear 已被改成 -2
- **叠加第二坑**:lambda 参数名就叫 print,遮蔽内置 print;oski(abs) 把 abs 绑给参数 print,函数体 `print(bear)` 实际等价 `abs(bear)`
- **结果**:`abs(-2)=2`,且控制台什么都不打印(内置 print 从未被调用)
- **结论**:闭包存的是 frame 引用而非值快照;晚绑定

> **桥 4→5**:lambda 是这个陷阱的载体;lambda 与 def 在环境图上的差异正好被这道题暴露。

### 层 5:lambda 表达式——没有内在名字的函数

- lambda 是表达式,只能写一个返回表达式,不能多条语句
- **环境图差异**:def 创建函数时名字与对象同一步绑死;lambda 创建的函数对象图上标 λ(无 intrinsic name),只有赋值给变量时名字才"借"给它
- 同一 lambda 赋给两个变量,函数对象仍只有一个,两个变量只是分别指向它

> **桥 5→6**:lambda 让 currying 的写法更紧凑(嵌套 lambda)。

### 层 6:柯里化——闭包的一个具体应用

- 把多参数函数拆成一串单参数函数,各自记住前面参数
- `curried_add(2)` 创建 g,g 的 parent 是 curried_add 这次调用的局部 frame(含 x=2);g(3) 沿链查到 x=2 算出 5。与 make_adder 同构
- lambda 版:`curried_add = lambda x: lambda y: x + y`
- **目的**:部分应用(partial application)——配合 map/filter 这类只接受单参数函数的场景,提前锁定部分参数得到可复用单参数函数

> **桥 6→7**:currying 让 Jace 重新审视 HOF 的定义边界。

### 层 7:修正高阶函数的定义

- **HOF 定义**:接受函数作参数 OR 返回函数作返回值,满足任一即可
- **订正**:"返回函数" ≠ "一定创建了闭包"
- **反例 select_function**:从已有函数里选一个返回,无新函数对象、无闭包
- 入参是函数这一支在 CS61A 术语里无单独名字,叫 "functions as arguments",对应 Strategy Pattern

## 我的理解(保留原话)

Jace 看完视频后回报的 6 点(原话,展示真实理解状态):

> 1. "先应该是想要说高级函数的环境图,介绍了一个 apply_twice 的函数 用于接受一个函数和参数 并连续俩次调用,他演示了一下函数图 但是感觉有点奇怪 在 apply_twice 这个函数里调用的某参数函数,为啥他的 parent 也是 Global 啊?我在想这个 parent 实际是 def 定义好的难道是这样? 那它怎么拿到 apply_twice 里的绑定?"
> 2. "嵌套定义,也就是指的是返回一个方法对吧,实际就是个装饰器,在环境图里我发现函数对象的父框架是它创建时的当前框架,说了一堆我没听懂的"
> 3. "局部变量名:加入不用嵌套定义的方式,而是在 global 里定义俩个函数 这样就找不到对应的变量名了"
> 4. "函数组合:做了几个函数组合的例子,然后说了一下函数图,到目前 为啥说了这么多这些?到底是为了什么?"
> 5. "lambda 表达式:感觉这东西和 def 没啥区别啊?也就是功能受限了 只有一行?似乎环境图也有一点点区别,区别在于一个在 def 就有了名字,另一个在赋值时才有名字"
> 6. "柯里化:完全不懂这在干什么?以及为什么设计这些东西 完全不懂。以及最后用 lambda 方式弄出来一样的东西 完全不懂。似乎说的是将多参数函数转换成单参数函数的技术?但这个在 java 开发中似乎很常见?"

**Link 笔记里"我的理解"段定稿**(共同推导后整理):

> 这节课的起点是:函数能被传来传去之后,光靠直觉读代码会出错,典型反例就是 bear/oski 那道题——直觉上以为闭包记住的是值,实际记住的是 frame。要解决这个问题,需要把环境模型变成两条死规则:定义时确定 parent(拿钥匙),调用时开新 frame 并复用那把钥匙(开箱子)。
>
> 这两条规则解释了我一开始觉得奇怪的地方:apply_twice 内部调用的函数,parent 还是 Global,因为 parent 只认定义位置,不认调用位置——这就是词法作用域。同样的规则反过来用,就能解释为什么嵌套定义能产生闭包:内层函数的 parent 是外层函数那次调用的局部 frame,所以能'记住'外层的局部变量;如果不嵌套,这条链就断了。
>
> lambda 和 def 的区别本质上是表达式和语句的区别,体现在环境图上就是 lambda 没有内在名字。柯里化则是把闭包机制包装成'链式调用、部分应用'这种实用形式,目的是配合 map/filter 这类只接受单参数函数的场景。最后,select_function 这个反例提醒我:HOF 的'返回函数'分支,不等于一定用了闭包,这是定义本身和具体实现手段的区别。

**关键推导点的上下文**:
- **apply_twice 父帧困惑**:Jace 自行猜测"我在想这个 parent 实际是 def 定义好的难道是这样?" → Claude 确认"你猜对了——parent 是 def(或 lambda)被定义那一刻就定死的,跟谁调用它、在哪调用它没关系。"并补反向验证"如果 square 函数体里用了一个只在 apply_twice 局部变量里才有的名字,会怎样?——找不到,报错。"
- **嵌套是闭包必要条件**:Jace #3 自行推导"不嵌套在 global 里定义两个函数就找不到变量名" → Claude 确认"这正是为什么必须嵌套定义才能做出闭包:不嵌套,parent 链就接不到那个局部变量上。"
- **bear/oski 证明闭包存帧引用**:Jace 起初以为 abs 是 typo("abs 是啥 你是不是写错了"),经澄清后说"了解了"
- **currying 作为闭包机制的实际应用**:Jace"完全不懂" → Claude 用 make_adder 同构解释"柯里化不是新机制,就是你刚搞懂的'嵌套定义产生闭包'的一个具体用法",并落到部分应用配合 map/filter
- **lambda 像受限的 def**:Jace #5 → Claude 确认并深化为"lambda 是表达式,只能写一个返回表达式;环境图上的区别就是 def 创建的函数在'创建'这一步就直接绑定到名字上,lambda 创建的函数对象本身没名字(标注成 λ)"

## Java 桥梁

- **函数作为参数 → Strategy Pattern**:"把'变化的计算规则'抽象成参数,对应 Java 的 Strategy Pattern(如 Collections.sort 传 comparator)"
- **函数作为返回值(闭包)→ Decorator Pattern**:"返回函数的真正动机:当目标框架的接口签名被固定(如只接受单参数函数),用闭包把额外上下文'预先绑定'进去再传入,对应 Java 的 Decorator Pattern(如 @trace、BufferedInputStream 包 FileInputStream)"
- **词法作用域 Java 对照**:"Java 里也一样,匿名类/lambda 捕获的是它被创建时所在的上下文,不是后来谁调用了它。"
- **bear/oski 与 Java effectively final 对照**:"这个问题跟 Java lambda 要求 'effectively final' 变量直接相关" —— the lambda sees the updated value when called, not a snapshot from definition time. This late binding behavior is a key distinction from languages like Java where lambda variables must be effectively final, capturing the actual value rather than the name.
- **currying Java 同构**:"你提到 Java 里见过类似的,是不是这种:`Function<Integer, Function<Integer, Integer>> curriedAdd = x -> y -> x + y;`?如果是,结构跟 Python 这个一模一样,本质都是'返回函数的函数',Java 只是用嵌套的 Function 接口类型把这条'链'显式写出来了。"

## Lab/HW 答题过程

**本次对话没有 Lab 02 的实际答题推导过程。** Lab 02 仅作为资源链接被提供,对话中未进入具体题目作答。Claude 明确说 currying"是 Lab 02 的练习内容(对应教材 1.6.5),等看完这节课我们可以单独补一轮",即留待后续单独处理。

**三个 Consume 引导问题的最终作答**(Jace 确认理解后给出):

1. **"定义时规则 = 拿钥匙"**:函数被定义那一刻,就记下了'它将来能看到哪个 frame'——这把钥匙就是它的 parent 标签,从此定死,不会因为后来被谁调用而变。**"调用时规则 = 开新箱子"**:每次被调用,都新开一个独立的局部 frame(box),这个新 box 的 parent 抄的就是函数当初拿到的那把钥匙——跟这次是谁调用、在哪调用完全无关。
2. **bear/oski 答案**:`oski(abs)` 算出来是 `abs(-2)=2`,不会打印任何东西(局部的'print'被参数名遮住了)。说明闭包记住的是 frame(一条能查到 bear 的路径),不是 bear 当时的值——是调用时才真正去查,不是定义时就锁死。
3. **lambda 的标注**:标的是 λ,不是变量名。说明 lambda 创建出来的函数对象本身没有'内在名字'——def 创建函数时,名字和函数对象在'定义'这一步就绑死了;lambda 创建的函数对象一开始是匿名的,只有后来被赋值给某个变量,才'借'了那个变量的名字,函数对象本身依然只有一个,变量只是指向它。

## 关键纠错与突破

**Claude 主动纠正**:

1. **编号争议**:坚持用官方 Lecture 5 而非 Jace 想的 4(论证依据见上文)
2. **abs 不是 typo(核心澄清)**:Jace"abs 是啥 你是不是写错了" → Claude:"不是写错,这是官方 slides 里原题。abs 在这里就是故意挖的坑,而且这道题埋了两个坑,不是一个。"完整澄清:
   > 先看 lambda 的参数名:oski = lambda print: print(bear)。这个 lambda 的参数名字就叫 'print'。这意味着在 oski 的函数体内部,'print' 这个名字会被局部 frame 里的绑定遮住——它不再指向 Python 内置的 print 函数,而是指向你调用 oski 时传进来的那个参数。所以 oski(abs) 做的事情是:把 abs 绑定给参数 'print'。执行函数体 print(bear) 时,这里的 'print' 查到的是局部 frame 里的 abs,不是内置 print。于是这一行实际等价于 abs(bear)。bear 这时候是多少?往上查到 Global,Global 里 bear 已经被改成 -2 了(因为是调用时才查,不是定义时)。所以最终算出来的是 abs(-2),也就是 2。整个 oski(abs) 是一个表达式,求值结果是 2——它不会在控制台打印任何东西,因为内置的 print 根本没被调用到。这道题故意把'晚绑定查找 bear'和'参数名遮住内置函数名'这两个坑叠在一起,就是为了逼你严格按 frame 规则走,不能凭名字'看起来像什么'去猜。
3. **"返回函数" ≠ "嵌套函数"**:Jace 以为"返回值是方法就是嵌套函数" → "'返回值是函数' ≠ '嵌套函数',这俩不完全等价:'返回值是函数'是行为层面的描述;'嵌套定义'是实现这个行为的一种常见手段。但也存在'返回函数、但没有嵌套、也没有闭包'的情况。"给出 select_function 反例
4. **CLIP 顺序自纠**:中途直接说"走 Internalize",后自行纠正——"按 CLIP 的顺序,下一步其实是 Link"
5. **.md 文件交付纠错**:第一稿给了纯聊天文本,Jace"怎么没有 md 啊 我是给 obsidian 用的 你是不是都忘了" → 改为生成真正的 .md 文件

**Jace 的啊哈时刻**:
- apply_twice 父帧:从"为啥 parent 也是 Global"的困惑,自猜"parent 实际是 def 定义好的",被确认后贯通到词法作用域
- bear/oski:从以为 abs 是笔误,到理解"两个坑叠加"(参数名遮蔽 + 晚绑定),回复"了解了"
- currying:从"完全不懂这是在干什么"到理解"就是嵌套定义产生闭包的一个具体用法",并接上 Java 的 `Function<Integer, Function<Integer, Integer>>` 同构
- 嵌套必要性:自行推出"不嵌套就找不到变量",被确认为闭包成立的必要条件而非风格选择

## 相关概念

- [[04 - Higher-Order Functions]] — 前置:函数可传入/传出,本讲把环境模型正式化以机械追踪这些操作;并落实 L4 留的 Lambda、Currying 待办
- [[03 - Control]] — 父帧地址概念的源头,本讲是其在闭包场景的精确化
- [[02 - Functions]] — 环境/帧的最初定义
