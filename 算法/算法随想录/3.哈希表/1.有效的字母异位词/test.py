from typing import Dict
from collections import defaultdict, Counter


# ==================== 思路 1：双重循环 + 删除字符（最原始暴力） ====================
def isAnagram_bruteforce(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    lst_t = list(t)
    for c in s:
        if c in lst_t:
            lst_t.remove(c)
        else:
            return False
    return True


# ==================== 思路 2：排序后对比（简易暴力） ====================
def isAnagram_sort(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    return sorted(s) == sorted(t)


# ==================== 思路 3：数组哈希（最优，26 小写字母专用） ====================
def isAnagram_array(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    record = [0] * 26
    for c in s:
        record[ord(c) - ord('a')] += 1
    for c in t:
        record[ord(c) - ord('a')] -= 1
    for num in record:
        if num != 0:
            return False
    return True


# ==================== 思路 4-1：字典哈希 defaultdict（通用） ====================
def isAnagram_dict(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    count = defaultdict(int)
    for c in s:
        count[c] += 1
    for c in t:
        count[c] -= 1
    for v in count.values():
        if v != 0:
            return False
    return True


# ==================== 思路 4-2：字典哈希 Counter（语法糖） ====================
def isAnagram_counter(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)


if __name__ == "__main__":
    print("=" * 60)
    print("LeetCode 242 - 有效的字母异位词")
    print("=" * 60)

    # (描述, s, t, 期望结果)
    test_cases = [
        # 官方示例
        ("官方示例1：true", "anagram", "nagaram", True),
        ("官方示例2：false", "rat", "car", False),

        # 数量不对称
        ("a多b少", "aab", "abb", False),
        ("完全相同", "hello", "hello", True),

        # 边界情况
        ("双空串", "", "", True),
        ("单字符相同", "a", "a", True),
        ("单字符不同", "a", "b", False),

        # 长度不等（直接剪枝）
        ("长度不等", "abc", "abcd", False),

        # 所有字母都涉及
        ("全字母乱序", "abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba", True),

        # 长重复字符
        ("大量重复", "aaaaabbbbbccccc", "cccccbbbbbaaaaa", True),
        ("大量重复少一个a", "aaaaabbbbbccccc", "aaaabbbbbccccc", False),
    ]

    solutions: Dict[str, callable] = {
        "双重循环暴力  ": isAnagram_bruteforce,
        "排序暴力     ": isAnagram_sort,
        "数组哈希最优  ": isAnagram_array,
        "字典哈希     ": isAnagram_dict,
        "Counter 哈希 ": isAnagram_counter,
    }

    all_passed = True
    for sol_name, sol_func in solutions.items():
        print(f"\n📦 解法: {sol_name}")
        print("-" * 40)

        for name, s, t, expected in test_cases:
            result = sol_func(s, t)
            passed = result == expected
            if not passed:
                all_passed = False

            status = "✅" if passed else "❌"
            # 太长时截断显示
            show_s = s if len(s) <= 20 else s[:17] + "..."
            show_t = t if len(t) <= 20 else t[:17] + "..."
            print(f"  [{name}]")
            print(f"    s={show_s!r}  t={show_t!r}")
            print(f"    输出={result}  期望={expected}  {status}")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有解法 × 全部用例 通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 60)
