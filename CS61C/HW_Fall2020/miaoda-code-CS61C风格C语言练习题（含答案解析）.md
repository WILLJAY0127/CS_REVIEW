# CS61C 风格 C 语言练习题（含答案解析）
> 说明：贴合 CS61C 重点，不考文件IO、复杂宏；核心考点：类型、补码、位运算、指针、数组、struct对齐、malloc、函数指针
> 编译推荐：gcc -Wall -Wextra -g，配合 gdb、valgrind
> 约定：32位 int，指针4字节；char=1，short=2；默认小端；有符号溢出为未定义行为；无符号按模运算

---

## 第一组：类型、无符号、移位、位运算
### Q1
预测输出：
```c
#include <stdio.h>
int main() {
    unsigned int a = 10;
    int b = -20;
    if (a + b > 0) {
        printf("yes\n");
    } else {
        printf("no\n");
    }
    return 0;
}
```

<details>
<summary>答案 & 解析</summary>
输出：`yes`

解析：`unsigned` 和 `int` 运算时，`int` 会隐式转换为 `unsigned`。`(unsigned)-20` 是一个很大的正数，10 + 这个大数结果 > 0。
</details>

### Q2
写一个函数 `int get_bit(int x, int n)`
返回 x 的第 n 位（从0开始，最低位是bit0）是0还是1。
要求只用位运算，不用if。

<details>
<summary>答案 & 解析</summary>
```c
int get_bit(int x, int n) {
    return (x >> n) & 1;
}
```
解析：右移n位把目标bit挪到最低位，再和1按位与取出该bit。
</details>

### Q3
写 `int set_bit(int x, int n, int v)`
把x第n位设置成v（v只能是0或1），返回新值。

<details>
<summary>答案 & 解析</summary>
```c
int set_bit(int x, int n, int v) {
    if (v) {
        return x | (1 << n);
    } else {
        return x & ~(1 << n);
    }
}
```
解析：v=1 用或运算置1；v=0 先构造掩码，与运算清零。
</details>

---

## 第二组：指针 & 数组（高频坑：数组不是指针）
### Q4
预测输出：
```c
#include <stdio.h>
void func(int arr[]) {
    printf("%zu\n", sizeof(arr));
}
int main() {
    int a[5] = {1,2,3,4,5};
    printf("%zu\n", sizeof(a));
    func(a);
    return 0;
}
```
> 注意：`%zu` 打印 size_t

<details>
<summary>答案 & 解析</summary>
输出：
```
20
4
```
解析：`sizeof(a)`：数组一共5个int，5*4=20；
数组作为函数参数时**退化为指针**，`sizeof(arr)` 得到指针大小（4字节）。
</details>

### Q5
```c
#include <stdio.h>
int main() {
    char s[] = "hello";
    char *p = "hello";
    s[0] = 'x';
    // p[0] = 'y';
    printf("%s\n", s);
    return 0;
}
```
1. 如果取消注释 `p[0] = 'y'` 会发生什么？为什么？
2. `s` 和 `p` 在内存分区上有什么区别？

<details>
<summary>答案 & 解析</summary>
1. 会触发段错误（segfault），未定义行为。字符串字面量存放在只读段，不允许修改。
2. `s` 是栈上的字符数组，可读写；`p` 只是指针，指向 `.rodata` 只读段里的字符串字面量。
</details>

### Q6
实现 `void swap(int *x, int *y)`，交换两个int的值。
思考题：直接传 `int x, int y`（值传递）能不能在函数内交换main里的变量？为什么？

<details>
<summary>答案 & 解析</summary>
```c
void swap(int *x, int *y) {
    int tmp = *x;
    *x = *y;
    *y = tmp;
}
```
值传递版本不行：函数拿到的只是副本，修改副本不会影响main中原变量。
</details>

### Q7
判断对错 + 解释：
`a[i] == *(a+i)`，所以 `a` 和 `&a[0]` 完全等价，数组就是指针。

<details>
<summary>答案 & 解析</summary>
前半句 `a[i] == *(a+i)` ✅ 正确；
后半句 ❌ 错误：**数组不是指针**。
数组拥有独立存储空间；`sizeof(数组)` 和 `sizeof(指针)` 结果不一样。数组名只是在绝大多数表达式场景下隐式退化成首元素地址。
</details>

---

## 第三组：struct、union、内存对齐（padding）
> 假设：char=1, short=2, int=4

### Q8
```c
struct S1 {
    char c;
    int i;
};
struct S2 {
    int i;
    char c;
};
```
求 `sizeof(struct S1)` 和 `sizeof(struct S2)`，标出padding。

<details>
<summary>答案 & 解析</summary>
- sizeof(struct S1) = 8
  布局：char(1) + padding(3) + int(4)
- sizeof(struct S2) = 8
  布局：int(4) + char(1) + padding(3)

对齐规则：成员对齐到自身大小的倍数；整个结构体对齐到最大成员大小。
</details>

### Q9
```c
union U {
    int i;
    char c;
};
```
- `sizeof(union U)` 是多少？
- 如果小端机器，`union U u; u.i = 0x12345678;`，`u.c` 的值是多少？

<details>
<summary>答案 & 解析</summary>
sizeof(union U) = 4（取最大成员的大小）
小端下：`u.c = 0x78`
解析：union所有成员共享同一块内存；小端低字节放在低地址。
</details>

---

## 第四组：动态内存 malloc / free / 悬垂指针 / 内存泄漏
### Q10
找出下面代码所有bug（valgrind可捕获）
```c
#include <stdio.h>
#include <stdlib.h>
int* bad_func() {
    int x = 100;
    return &x;
}
int main() {
    int *p = bad_func();
    printf("%d\n", *p);

    int *q = malloc(4);
    free(q);
    free(q);
    return 0;
}
```

<details>
<summary>答案 & 解析</summary>
1. 返回局部栈变量地址 → 悬垂指针；函数返回后栈帧销毁，访问非法。
2. double free：同一个指针连续free两次，未定义行为。
3. 缺少malloc返回值判空（工程规范）。
</details>

### Q11
写一个函数：`int* make_array(int n)`
分配n个int的堆数组，全部初始化为0，返回首地址。
说明调用方注意事项。

<details>
<summary>答案 & 解析</summary>
```c
int* make_array(int n) {
    int *arr = malloc(n * sizeof(int));
    if (!arr) return NULL;
    for(int i=0;i<n;i++) arr[i]=0;
    return arr;
}
```
调用方用完必须 `free(arr);`；忘记free会造成内存泄漏。
</details>

### Q12（悬垂指针）
```c
int *p;
{
    int arr[3] = {1,2,3};
    p = arr;
}
// 到这里，*p 还合法吗？为什么？
```

<details>
<summary>答案 & 解析</summary>
不合法。arr是代码块内栈上局部数组，代码块结束栈内存回收，p变成悬垂指针。
</details>

---

## 第五组：argc, argv + 函数指针
### Q13
```c
#include <stdio.h>
int main(int argc, char **argv) {
    printf("%s\n", argv[0]);
    return 0;
}
```
运行：`./a.out apple banana`
输出是什么？argc等于几？

<details>
<summary>答案 & 解析</summary>
argc = 3
argv[0] 输出程序名：`./a.out`
argv[1] = "apple"，argv[2] = "banana"
</details>

### Q14（函数指针）
定义函数指针 `calc_fp`，它指向一个接收两个int、返回int的函数。
写add、sub两个函数，用函数指针数组，根据下标选择计算。

<details>
<summary>答案 & 解析</summary>
```c
#include <stdio.h>
int add(int a, int b) { return a+b; }
int sub(int a, int b) { return a-b; }

typedef int (*calc_fp)(int, int);
int main() {
    calc_fp fns[] = {add, sub};
    printf("%d\n", fns[0](3,5));
    printf("%d\n", fns[1](3,5));
    return 0;
}
```
</details>
