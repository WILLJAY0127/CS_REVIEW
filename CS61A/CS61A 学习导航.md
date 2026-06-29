# CS61A 学习导航

> 用 [[clip-study-method|CLIP 学习法]] 系统学习 UC Berkeley CS61A。
> 参考站:[insideempire archive](https://insideempire.github.io/CS61A-Website-Archive/) · [cs61a.org](https://cs61a.org) · [composingprograms.com](https://composingprograms.com)
> 编号规则:**用归档站官方讲次编号,不中途重排**。

## 讲次笔记(知识主存)

按 CLIP-L 标准组织:总问题 → 分层推进(带层间桥梁)→ "我的理解"(费曼推导链原话)→ Java/设计模式桥梁 → HW/Lab 答题过程(纠错不直接给答案)→ 相关概念。

| 讲次 | 标题 | 状态 | 笔记 |
|---|---|---|---|
| Lec 2 | Functions | ✅ C/L/I/P 全完成 | [[02 - Functions]] |
| Lec 3 | Control | ✅ C/L/I/P 全完成 | [[03 - Control]] |
| Lec 4 | Higher-Order Functions | ✅ C/L/I/P 全完成 | [[04 - Higher-Order Functions]] |
| Lec 5 | Environments | 🔶 L+I 完成,P(Lab02)待补 | [[05 - Environments]] |
| Lec 6+ | (递归等) | ⏳ 未开始 | [[递归]] (仅占位两行) |

## 总问题速览(每讲一句话)

- **Lec 2 Functions**:你写下 `add(2, 3)`,计算机怎么知道这是什么意思?
- **Lec 3 Control**:Python 默认顺序执行,Control 如何引入"判断"与"重复"——背后的统一执行模型是什么?
- **Lec 4 HOF**:如果函数本身可以像数字一样被传进、传出,抽象的力量能走多远?
- **Lec 5 Environments**:有没有一套不依赖直觉、机械地追踪任何涉及函数传递的代码的方法?

## 贯穿主线(已建立的知识链)

```
Lec2: 原始值 → 表达式 → 名字绑定 → 函数定义 → 环境/帧 → 纯vs非纯(副作用逃出帧)
   ↓
Lec3: 帧是名字→值表 → 语句vs表达式 → 函数对象三件套(形参表+函数体+父帧地址)
   ↓ (父帧地址在更复杂场景下的延伸)
Lec4: 函数当参数(Strategy) → 函数当返回值(闭包=函数对象+环境帧,Decorator) → 一等公民
   ↓ (把环境模型正式化成画图规则)
Lec5: 定义时定 parent(拿钥匙) → 调用时开新 frame(开箱子) → 词法作用域
      → 嵌套是闭包必要条件 → 闭包存 frame 引用非值快照(bear/oski) → lambda 无内在名 → currying
```

## Jace 自己推导出的核心洞察(不在课本里)

- **副作用 = 逃出帧的东西**(Lec2,I 阶段)
- **一行代码要求步骤之间没有依赖性**(Lec2,P 阶段 two_of_three)→ 连到表达式树/函数式编程
- **父帧地址 = 定义它的帧,不是调用它的帧**(Lec4,词法 vs 动态作用域)
- **闭包 = 函数对象 + 它出生时捕获的环境帧**(Lec4)
- **传出是手段,传入才是目的**(Lec4,返回函数的动机)
- **函数急切求值 vs 控制语句惰性求值,不可替代**(Lec4)

## 原始对话档案(过程留底)

所有 Claude.ai 旧对话已抽取成可读 markdown,留作复盘"当时为什么卡住"用:
- 索引:`CS61A/claude对话/extracted/README.md`
- CS61A 相关 5 份:`03_` / `06_` / `08_` / `12_` / `13_`
- 原始机器格式导出(`data-*/`,5.8MB,不可读)已从 git 排除

## 待办

- [ ] Lec 5 的 Lab 02 实际答题(P 阶段)
- [ ] Lec 6+ 递归等后续讲次(现有 `递归.md` 仅两行占位,做到那讲时按 CLIP 补全)
