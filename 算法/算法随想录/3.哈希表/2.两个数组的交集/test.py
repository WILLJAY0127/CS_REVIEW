from typing import List, Dict


# ==================== 思路 1：最原始暴力（双重循环 + 手动去重） ====================
def intersection_bruteforce(nums1: List[int], nums2: List[int]) -> List[int]:
    res = []
    for n1 in nums1:
        for n2 in nums2:
            if n1 == n2:
                if n1 not in res:
                    res.append(n1)
                break
    return res


# ==================== 思路 2：哈希集合 set（刷题首选） ====================
def intersection_set(nums1: List[int], nums2: List[int]) -> List[int]:
    set1 = set(nums1)
    res = []
    for num in nums2:
        if num in set1:
            res.append(num)
            set1.remove(num)
    return res


# ==================== 思路 2-2：用结果 set 去重的变体（不删除原 set1） ====================
def intersection_set2(nums1: List[int], nums2: List[int]) -> List[int]:
    set1 = set(nums1)
    res_set = set()
    for num in nums2:
        if num in set1:
            res_set.add(num)
    return list(res_set)


# ==================== 思路 3：数组哈希（数值范围有限时） ====================
def intersection_array(nums1: List[int], nums2: List[int]) -> List[int]:
    # 范围 0~1000（大多数 LC 测试用例满足；题目没给范围仅作模型演示）
    MAX_VAL = 1001
    record = [0] * MAX_VAL

    for n in nums1:
        if 0 <= n < MAX_VAL:
            record[n] = 1

    res = []
    for n in nums2:
        if 0 <= n < MAX_VAL and record[n] == 1:
            res.append(n)
            record[n] = 0
    return res


# ==================== 思路 4：双指针排序法（时间换空间） ====================
def intersection_two_pointers(nums1: List[int], nums2: List[int]) -> List[int]:
    nums1.sort()
    nums2.sort()

    i = j = 0
    res = []
    n1, n2 = len(nums1), len(nums2)

    while i < n1 and j < n2:
        a, b = nums1[i], nums2[j]
        if a < b:
            i += 1
        elif a > b:
            j += 1
        else:
            res.append(a)
            # 跳过 nums1 全部重复值
            while i < n1 and nums1[i] == a:
                i += 1
            # 跳过 nums2 全部重复值
            while j < n2 and nums2[j] == a:
                j += 1
    return res


if __name__ == "__main__":
    print("=" * 60)
    print("LeetCode 349 - 两个数组的交集")
    print("=" * 60)

    def is_correct(result: List[int], expected: List[int]) -> bool:
        """结果去重比较（顺序不敏感）"""
        return sorted(result) == sorted(expected)

    # (描述, nums1, nums2, 期望)
    test_cases = [
        ("官方示例1", [1, 2, 2, 1], [2, 2], [2]),
        ("官方示例2", [4, 9, 5], [9, 4, 9, 8, 4], [9, 4]),
        ("无交集", [1, 2, 3], [4, 5, 6], []),
        ("一边空", [], [1, 2], []),
        ("两边空", [], [], []),
        ("完全相同且重复", [7, 7, 7, 7], [7, 7, 7], [7]),
        ("nums1 全不重复", [1, 3, 5, 7], [7, 5, 3, 1], [1, 3, 5, 7]),
        ("重复多次命中", [2, 2, 3, 3, 3], [2, 2, 2, 3], [2, 3]),
        ("大数字", [100, 200, 300], [300, 400, 100], [100, 300]),
        ("范围正好卡数组哈希", [0, 1, 1000], [1, 1000, 0], [0, 1, 1000]),
    ]

    solutions: Dict[str, callable] = {
        "双重循环暴力  ": intersection_bruteforce,
        "哈希集合（删） ": intersection_set,
        "哈希集合（存） ": intersection_set2,
        "数组哈希     ": intersection_array,
        "双指针排序法  ": intersection_two_pointers,
    }

    all_passed = True
    for sol_name, sol_func in solutions.items():
        print(f"\n📦 解法: {sol_name}")
        print("-" * 40)

        for name, nums1, nums2, expected in test_cases:
            result = sol_func(list(nums1), list(nums2))  # 传副本，防止 sort 破坏原数据
            passed = is_correct(result, expected)
            if not passed:
                all_passed = False

            status = "✅" if passed else "❌"
            # 过长截断
            def show(x):
                return str(x) if len(str(x)) < 40 else str(x[:35]) + "..."
            print(f"  [{name}]")
            print(f"    nums1={show(nums1)}")
            print(f"    nums2={show(nums2)}")
            print(f"    输出={sorted(result)}  期望={sorted(expected)}  {status}")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有解法 × 全部用例 通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 60)
