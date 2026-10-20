# 消息传递：从 CS61A 的 dispatch 到 class 与 IoC

> 来源锚点：[CS61A_知识库总览.md](file:///d:/myfile/CS_REVIEW/快速学习版本/CS61A/CS61A_知识库总览.md) 第 8 条——"对象不是面向对象的重点，消息传递才是"。
> 本文定位：补足总览里"核心概念 → 8. 面向对象"这一节缺掉的**消息传递**主线，把它从 CS61A 一路接到你正在学的 Python class 和 Java/Spring。

## 8+1 总览卡

1. **一句话**：`class` 不是面向对象的起点，它只是"消息传递"机制的**语法糖**。
2. **CS61A 的教学顺序**：先不给 `class`，用闭包 + dispatch 手搓一个对象系统，**造出来之后**才告诉你 class 在自动化同一件事。
3. **核心机制三件套**：消息传递（messaging）+ 状态藏在对象内（hiding of state）+ 运行期才决定谁响应（late binding）。
4. **手搓版的对象长什么样**：不是一个"装字段的数据袋"，而是一个**能对消息作出反应的函数**。
5. **换语言不换思想**：CS61A 的 Python 版和 SICP 的 Scheme 版是同一件事，只是闭包和语法的写法不同。
6. **Python 收口**：`obj.attr` 就是"发一条名叫 attr 的消息"，属性查找 = 分发，`__getattr__` = 拦截未定义的消息。
7. **Java 收口**：虚方法调用机制上就是消息（晚绑定）；Spring IoC 是同一机制在**框架层**的落地。
8. **一条判据**：写出 `a.getX().getY().getZ()` 时，你在"操作数据结构"，不在"发消息"——该停下来。

**一句话**：对象系统的本质是"发消息 + 收消息方自行决定怎么反应"，class、interface、IoC 都只是这句话在不同层次上的封装。

---

## 一、动机：为什么 CS61A 先讲 dispatch，不讲 class

如果一上来就教 `class`，你会把"面向对象"理解成**名词建模**——"世界由一堆对象组成，对象有字段和方法"。于是设计重心落在**"有哪些对象"**上，写出一堆 getter/setter，把内部状态暴露出去。

CS61A 反着来：**先给你一个没有 class 的对象系统**。当你亲手用函数造出"对象"后，才会看到——**真正让对象系统转起来的，是"发消息、按消息做反应"这个机制**；`class` 只是把这套机制包装得更顺手。

---

## 二、CS61A 版：用闭包手搓一个对象系统

```python
def make_account(balance):
    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return 'Insufficient funds'
        balance -= amount
        return balance

    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance

    def dispatch(message):
        if message == 'withdraw':
            return withdraw
        elif message == 'deposit':
            return deposit
        else:
            raise ValueError('Unknown message: ' + message)

    return dispatch

acc = make_account(100)
acc('withdraw')(30)      # 先发消息 'withdraw' 拿回方法，再调用
```

**环境模型走查**（对照总览里的"卡片 B：环境模型"）：

1. `make_account(100)` 建帧 E1，`balance = 100`；
2. 返回 `dispatch` 函数对象，其 `parent = E1`；E1 因被引用而存活 → **这就是闭包**；
3. `acc('withdraw')` 建帧 E2，`message = 'withdraw'`，返回 `withdraw`（其 `parent` 仍指向 E1）；
4. `(30)` 建帧 E3，`amount = 30`；`nonlocal balance` 改的是 **E1 里的 balance**。

**三件事，正好对上 Kay 的定义**：

| 现象 | 对应机制 |
|---|---|
| `acc` 是函数、靠 `acc('withdraw')` 访问功能 | **消息传递** |
| `balance` 锁在 E1，外界拿不到 | **hiding of state** |
| 哪个函数被返回，只有运行时才知道 | **late binding** |

---

## 三、SICP / Scheme 版：同一思想，换个语法

CS61A 的源头 SICP 3.1 用 Scheme 写的是同一件事：

```scheme
(define (make-account balance)
  (define (withdraw amount)
    (if (>= balance amount)
        (begin (set! balance (- balance amount)) balance)
        "Insufficient funds"))
  (define (deposit amount)
    (set! balance (+ balance amount))
    balance)
  (define (dispatch m)
    (cond ((eq? m 'withdraw) withdraw)
          ((eq? m 'deposit) deposit)
          (else (error "Unknown request -- MAKE-ACCOUNT" m))))
  dispatch)
```

用法：`((acc 'withdraw) 30)`。对照 Python 版，差异只在语法：

| Python | Scheme |
|---|---|
| 闭包 + `nonlocal` | 闭包 + `set!` |
| `message == 'withdraw'` | `(eq? m 'withdraw)` |
| `acc('withdraw')` | `(acc 'withdraw)` |
| 返回函数对象 | 返回过程（procedure） |

**结论**：对象系统是**模式**，不是某个语言的专利——Python、Scheme 都能用"闭包 + 分发"造出来。

---

## 四、收口一：`class` 就是 dispatch 的语法糖（Python 语言层）

CS61A 讲完 dispatch 后会亮出 class，并点破二者是同一件事：

| 手搓 dispatch 版 | class 版 |
|---|---|
| `dispatch('withdraw')` | `acc.withdraw`（**属性查找**） |
| `dispatch('withdraw')(30)` | `acc.withdraw(30)`（**方法调用**） |
| 闭包变量 `balance` | `self._balance`（**实例属性**） |
| `if message == 'withdraw' ...` 分支 | `type(acc)` 上的方法表 / MRO 查找 |
| 未定义消息 → 报错 | `AttributeError`；可用 `__getattr__` 拦截 |

所以 **`obj.attr` 的语义就是"给 obj 发一条名叫 attr 的消息"**：先按"实例 → 类 → 基类 → object"的顺序查找，找到就返回；找不到才轮到 `__getattr__`。

```python
class Account:
    def __init__(self, balance):
        self._balance = balance
    def withdraw(self, amount):
        if amount > self._balance:
            return 'Insufficient funds'
        self._balance -= amount
        return self._balance
    def __getattr__(self, name):          # 只在常规查找失败时被调用
        raise AttributeError('Unknown message: ' + name)
```

`__getattr__` 就是"**拦截未定义的消息**"——和 dispatch 里那句 `raise ValueError('Unknown message')` 完全对应。

---

## 五、收口二：Java 里消息藏在哪（语言层 → 框架层）

**语言层**：Java 的 `obj.method()` 语法上像"调用"，但因为**虚方法是晚绑定的**，机制上就是消息——**运行期**由 `obj` 的真实类型决定跑哪份实现：

```java
Shape s = new Circle();
s.area();     // 编译期只知道"给 s 发 area 消息"，运行期才决定是 Circle.area
```

这也解释了 Java 里接口/多态为什么值钱：**发送方只依赖"消息协议"（接口），不依赖任何具体实现**。

**框架层**：Spring IoC/DI 是同一机制的放大——容器只负责"装配消息的接收方"，**谁来实现、怎么实现推迟到运行期**。这就是"Hollywood Principle：别找我们，我们会找你"。可对照你的 [Spring_IoC_DI核心概念_从EJB工艺到容器级单例.md](file:///d:/myfile/CS_REVIEW/interview/技能详解/tomcat/Spring_IoC_DI核心概念_从EJB工艺到容器级单例.md)。

---

## 六、一条判据：你在发消息，还是在操作数据结构？

**反例——穿透内部结构，这是操作数据结构：**

```java
order.getCustomer().getAddress().getCity();   // 发送方必须知道 3 层内部结构
```

**正例——只发一条有业务含义的消息：**

```java
order.shipTo(city);          // 怎么发货由 order 自己决定
shippingService.ship(order); // 谁发、怎么发由服务决定
```

**检验标准**：出现长串 `.getX().getY().getZ()` 时，说明发送方"伸手进别人身体里掏东西"了——把它改成一条消息（如 `shipTo`），内部结构就能自由变动，而调用方一行不改。这正是"可生长系统"的关键。

---

## 权威锚点

| 级别 | 来源 | 用途 |
|---|---|---|
| S | SICP 3.1（*Structure and Interpretation of Computer Programs*） | 消息传递式对象系统的原始出处 |
| S | CS61A 官方讲义（Object-Oriented Programming / Dispatch） | 本文代码与教学顺序的依据 |
| A | Alan Kay 1998 邮件（"OOP to me means only messaging..."） | "消息传递才是重点"的原始表述 |
| B | 你的 [CS61A_知识库总览.md](file:///d:/myfile/CS_REVIEW/快速学习版本/CS61A/CS61A_知识库总览.md) | 本文与之互补：总览给地图，本文展开一条线 |

---

## 与总览的关系

- 总览"核心概念 8. 面向对象"讲的是**属性查找 / 继承 / MRO**（机制细节）；
- 本文补的是**为什么这些机制存在**——它们都是"消息传递"的实现手段。
- 建议阅读顺序：先总览建立地图 → 再看本文理解 dispatch → 做 Ants 项目时，把 `action` 的多态分发看成"消息"，整个对象关系会立刻清晰。
