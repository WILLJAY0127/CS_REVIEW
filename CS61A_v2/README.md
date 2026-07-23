# CS61A 笔记体系 v2

四层学习法 + Weekly/Projects/Knowledge_Base 三层目录。当前学习阶段用 `Weekly/` 记新内容；学完整门课后再把 `Weekly/` 内容重构进 `Knowledge_Base/`。

## 目录说明

- `00_Overview.md` — 总览、讲次索引、术语索引入口
- `Weekly/` — 【当前主线】按讲次记笔记，每讲一个文件夹，用 `Weekly/_Template/` 复制新建
- `Projects/` — 独立大项目（Hog / Cats / Scheme Interpreter），不与周次笔记混杂
- `Knowledge_Base/` — 【远期】全部课程学完后，按教材章节主题重构，现在先不填
- `Common_Pitfalls.md` — 全局错题/易错点清单，持续更新

## 每讲固定流程

1. 看视频 → 记 `video_notes` 部分（讲师口头重点、类比、课件没写的坑）
2. 看 PPT → 记 `slides_notes` 部分（结构化定义、语法骨架）
3. 查教材对应章节 → 填 `textbook_correlate.md`（差异 + 拓展）
4. 做 Lab → HW → 写 `practice_summary.md`（考点、错误思路、正确思路、边界情况）
5. 遇到通用坑 → 同步补一条到根目录 `Common_Pitfalls.md`

## 新建一讲的笔记

复制 `Weekly/_Template/` 整个文件夹，改名为 `LecXX_标题/`（编号用官方讲次编号，不中途重排），然后照着模板填。`lecture_notes.md` 里已经把 `slides_notes` 和 `video_notes` 合并成一份，如果你后面发现还是想拆开，随时可以再拆成两个文件。

## 写作原则

- 理解优先，不追求排版好看；先把内容写完整，格式后面再调
- 不要照抄 PPT 原文，用自己的话重写定义——讲不出来就是没理解
- 代码只放笔记里的关键片段，完整代码放 `code/` 子文件夹
- 每讲写完，回 `00_Overview.md` 补一行索引
- 每周日花 30 分钟回顾本周笔记，不看资料尝试独立写出核心代码范式

## 历史存档

之前用 CLIP 学习法做的 Lec2-5 笔记和 `个人临时/` 草稿在 `../CS61A/`，不再更新，仅供回顾对照。
