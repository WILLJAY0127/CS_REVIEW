# CS61A ok 命令简易说明
> 适用自学玩家，解决运行 ok 时要求输入学校 edu 邮箱登录问题

## 基础原命令
```bash
python3 ok -q python-basics -u
```
### 参数拆解
1. `python3 ok`
运行当前目录下的 ok 评测程序（伯克利课程自动测试工具）
> ⚠️ 必须终端 `cd` 到包含 `ok` 文件的 lab 文件夹执行

2. `-q python-basics`
`-q` = question，指定只运行**单独一题**
后面 `python-basics` 替换成对应题目名称

3. `-u`
`-u` = unlock
用于打开 **WWPD 交互式问答题**（预测代码输出、选择题）
> 写代码函数自测时**不需要加 `-u`**

## 自学可用完整版（重点）
```bash
python3 ok -q python-basics -u --local
```
### `--local` 核心解释
- 默认不加 `--local`：ok 会联网连接伯克利服务器，强制要求 **berkeley.edu 教育邮箱登录**，自学没有账号会卡住。
- 加上 `--local`：**纯本地离线运行**，阻断所有网络请求，不需要登录、不用edu邮箱；仅在本机执行测试/交互问答，不会上传作业、进度到线上服务器。

## 常用模板整理
```bash
# 1、解锁交互式WWPD问答题（需要 -u + --local）
python3 ok -q 题目名 -u --local

# 2、写完代码，执行测试用例（不需要 -u）
python3 ok -q 题目名 --local

# 3、运行测试并展示完整详细日志（调试推荐）
python3 ok -q 题目名 -v --local

# 4、一次性执行当前lab所有题目
python3 ok --local
```

## 避坑提醒
1. **不要使用 `--submit`**
`--submit` 用于正式提交作业到伯克利评分系统，自学无法使用。
2. 命令执行前提：终端位置正确，文件夹内能看到 `ok` 文件。
3. Windows 如果 `python3` 报错，尝试替换命令开头为 `py` / `python`。

如果你想要精简版（去掉多余文字，只保留命令+极简注释）我可以再改一版。