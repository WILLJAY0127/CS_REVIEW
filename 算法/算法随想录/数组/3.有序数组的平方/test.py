from typing import List, Callable, Dict


def sortedSquares_brute(nums: List[int]) -> List[int]:
    for i in range(len(nums)):
        nums[i] *= nums[i]
    nums.sort()
    return nums


def sortedSquares_two_pointers(nums: List[int]) -> List[int]:
    n = len(nums)
    result = [0] * n
    k = n - 1
    left, right = 0, n - 1

    while left <= right:
        left_sq = nums[left] * nums[left]
        right_sq = nums[right] * nums[right]

        if left_sq < right_sq:
            result[k] = right_sq
            right -= 1
        else:
            result[k] = left_sq
            left += 1

        k -= 1

    return result


SOLUTIONS: Dict[str, Callable] = {
    "brute": sortedSquares_brute,
    "two_pointers": sortedSquares_two_pointers,
}

TEST_CASES = [
    ([-4, -1, 0, 3, 10], [0, 1, 9, 16, 100]),
    ([-7, -3, 2, 3, 11], [4, 9, 9, 49, 121]),
    ([0], [0]),
    ([1], [1]),
    ([-1], [1]),
    ([-5, -3, -2, -1], [1, 4, 9, 25]),
    ([1, 2, 3, 5], [1, 4, 9, 25]),
    ([-3, -2, -1, 0, 1, 2, 3], [0, 1, 1, 4, 4, 9, 9]),
]


def run_tests(solution: str = "two_pointers") -> None:
    if solution not in SOLUTIONS and solution != "all":
        print(f"❌ 未知解法: {solution}")
        print(f"   可选: {list(SOLUTIONS.keys())} 或 'all'")
        return

    if solution == "all":
        solutions_to_run = list(SOLUTIONS.items())
    else:
        solutions_to_run = [(solution, SOLUTIONS[solution])]

    print("=" * 60)
    print("LeetCode 977 - 有序数组的平方 测试")
    print("=" * 60)

    all_passed = True

    for sol_name, sol_func in solutions_to_run:
        print(f"\n📦 运行解法: {sol_name}")
        print("-" * 40)

        for i, (nums, expected) in enumerate(TEST_CASES):
            result = sol_func(nums.copy())
            passed = result == expected

            if not passed:
                all_passed = False

            status = "✅" if passed else "❌"
            print(f"  用例{i + 1}: {status}  输入 {nums} → 输出 {result}")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试用例通过！")
    else:
        print("❌ 部分测试用例失败，请检查代码")
    print("=" * 60)


if __name__ == "__main__":
    run_tests("two_pointers")
