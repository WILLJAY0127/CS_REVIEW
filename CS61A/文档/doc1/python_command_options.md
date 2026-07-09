# Python 命令行选项速查

## 常用命令

### 1. 直接运行文件

```bash
python3 lab00.py
```

- 执行文件中的代码
- 执行完毕后返回命令行
- 如果文件只包含函数定义，没有输出（除非有语法错误）

---

### 2. 交互式运行 (`-i`)

```bash
python3 -i lab00.py
```

- 执行文件中的代码后，进入交互式会话（`>>>` 提示符）
- 可以调用文件中定义的函数、测试表达式
- **退出方式**：
  - 输入 `exit()`
  - Linux/Mac: `Ctrl-D`
  - Windows: `Ctrl-Z Enter`
- **注意**：在交互式运行时修改文件，需要退出并重新启动才能生效

---

### 3. 运行 doctest (`-m doctest`)

```bash
python3 -m doctest lab00.py
```

- 运行文件中的 doctest（函数文档字符串中的示例）
- 每个测试由 `>>>` 开头的代码和预期输出组成
- **通过测试**：无输出
- **测试失败**：显示失败信息

---

## 示例

假设 `lab00.py` 包含：

```python
def twenty_twenty_four():
    """
    >>> twenty_twenty_four()
    2024
    """
    return (20 * 100) + (20 + 4)
```

**使用 `-i` 交互式测试**：

```bash
$ python3 -i lab00.py
>>> twenty_twenty_four()
2024
>>> exit()
```

**使用 `-m doctest` 测试**：

```bash
$ python3 -m doctest lab00.py
# 通过则无输出
```
