from typing import List


def minSubArrayLen_brute(target: int, nums: List[int]) -> int:
    """暴力解法：O(n²)"""
    n = len(nums)
    min_len = float('inf')

    for i in range(n):
        total = 0
        for j in range(i, n):
            total += nums[j]
            if total >= target:
                min_len = min(j - i + 1, min_len)
                break

    return min_len if min_len != float('inf') else 0


def minSubArrayLen(target: int, nums: List[int]) -> int:
    """滑动窗口解法：O(n)"""
    n = len(nums)
    min_len = float('inf')
    left = 0
    total = 0

    for right in range(n):
        total += nums[right]

        while total >= target:
            min_len = min(min_len, right - left + 1)
            total -= nums[left]
            left += 1

    return min_len if min_len != float('inf') else 0


if __name__ == "__main__":
    # ==================== LC209 测试 ====================
    print("=" * 60)
    print("LeetCode 209 - 长度最小的子数组")
    print("=" * 60)

    test_cases = [
        (7, [2, 3, 1, 2, 4, 3], 2),
        (4, [1, 4, 4], 1),
        (11, [1, 1, 1, 1, 1, 1], 0),
        (11, [1, 2, 3, 4, 5], 3),
        (15, [1, 2, 3, 4, 5], 5),
    ]

    all_passed = True
    for target, nums, expected in test_cases:
        result_brute = minSubArrayLen_brute(target, nums.copy())
        result_sliding = minSubArrayLen(target, nums.copy())

        brute_ok = result_brute == expected
        sliding_ok = result_sliding == expected
        if not brute_ok or not sliding_ok:
            all_passed = False

        status = "✅" if sliding_ok else "❌"
        print(f"  target={target}, nums={nums}")
        print(f"    暴力: {result_brute} {'✅' if brute_ok else '❌'}")
        print(f"    窗口: {result_sliding} {status}")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 LC209 所有测试通过！")
    else:
        print("❌ 部分测试失败")

    # ==================== 抽象练习：非求和滑动窗口 ====================
    print("\n" + "=" * 60)
    print("🧠 抽象练习：非求和滑动窗口")
    print("=" * 60)
    print("""
    【自定义题目】
    给定正整数数组 nums 和一个阈值 min_max，
    找出满足条件：子数组内元素的最大值 >= min_max 的
    最短连续子数组长度。如果不存在，返回 0。

    【关键观察】
    这个题目满足单调性吗？
    
    设窗口 [l, r]，窗口内最大值为 max_val：
    - 右边界扩展（r+1）：max_val 只会变大或不变 ✓
    - 左边界收缩（l+1）：max_val 只会变小或不变 ✓
    
    👉 满足单调性！可以用滑动窗口！
    """)

    # 练习解法：用滑动窗口
    def minSubArrayLen_by_max(min_max: int, nums: List[int]) -> int:
        """
        练习：用滑动窗口求「子数组最大值 >= min_max」的最短子数组
        时间复杂度：O(n²)（简化版，实际可优化到 O(n)）
        """
        n = len(nums)
        min_len = float('inf')
        left = 0

        for right in range(n):
            # 扩展窗口到 right
            current_max = max(nums[left:right + 1])

            # 收缩窗口：当最大值满足条件时
            while current_max >= min_max:
                # 更新答案
                min_len = min(min_len, right - left + 1)
                left += 1
                # 重新计算窗口内的最大值
                if left <= right:
                    current_max = max(nums[left:right + 1])
                else:
                    break

        return min_len if min_len != float('inf') else 0

    # 暴力解法：对比验证
    def minSubArrayLen_by_max_brute(min_max: int, nums: List[int]) -> int:
        """暴力解法：O(n²)"""
        n = len(nums)
        min_len = float('inf')

        for i in range(n):
            cur_max = 0
            for j in range(i, n):
                cur_max = max(cur_max, nums[j])
                if cur_max >= min_max:
                    min_len = min(min_len, j - i + 1)
                    break

        return min_len if min_len != float('inf') else 0

    # 测试
    practice_cases = [
        (5, [2, 3, 1, 5, 4], 1),      # 数字5本身，长度1
        (4, [2, 3, 1, 5, 4], 1),      # 数字4或5，最短1
        (6, [2, 3, 1, 5, 4], 0),      # 不存在（最大值才5）
        (3, [2, 3, 1, 5, 4], 1),      # 数字3本身，长度1
        (10, [2, 3, 1, 5, 4], 0),     # 不存在
        (3, [1, 1, 1, 1, 3], 1),      # 末尾的3
        (3, [1, 2, 2, 2, 3], 1),      # 直接命中
    ]

    print("\n【测试用例】")
    for min_max, nums, expected in practice_cases:
        result_brute = minSubArrayLen_by_max_brute(min_max, nums.copy())
        result_window = minSubArrayLen_by_max(min_max, nums.copy())

        brute_ok = result_brute == expected
        window_ok = result_window == expected

        status = "✅" if window_ok else "❌"
        print(f"\n  min_max={min_max}, nums={nums}")
        print(f"    期望:  {expected}")
        print(f"    暴力:  {result_brute} {'✅' if brute_ok else '❌'}")
        print(f"    窗口:  {result_window} {status}")

    print("\n" + "=" * 60)
    print("💡 思考题：")
    print("  1. 这个题目和 LC209 的解法有什么异同？")
    print("  2. 为什么左边界收缩时要重新计算最大值？")
    print("  3. 如何用单调队列优化到真正的 O(n)？")
    print("=" * 60)