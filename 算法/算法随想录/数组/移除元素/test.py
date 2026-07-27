from typing import List

# 移除坏人: 站在移除不要的数据的角度,站在这个视角上,一次事务的逻辑是 移除不要的,把剩下的填充上来
# 单数组视角,在原有基础上操作
def yichuHuairen(nums: List[int], target: int) -> int:
    i = 0
    over = len(nums)

    while i < over:
        if target == nums[i]:
            for j in range(i + 1, over):
                nums[j - 1] = nums[j]
            over -= 1
        else:
            i += 1

    return over
# 实际上是虚拟数组方式,或者双传送带方式
def haoren(nums: List[int],target: int) -> int:
    slow = 0

    for fast in range(len(nums)):
        if target != nums[fast]:
            # 理解成俩条独立的数组
            nums[slow] = nums[fast]
            slow += 1
    
    return slow



if __name__ == "__main__":
    test_cases = [
        ([3, 2, 2, 3], 3, [2, 2], 2)
        # ([0, 1, 2, 2, 3, 0, 4, 2], 2, [0, 1, 3, 0, 4], 5),
        # ([1, 1, 1], 1, [], 0),
        # ([1, 2, 3], 4, [1, 2, 3], 3),
        # ([], 1, [], 0),
        # ([1], 1, [], 0),
        # ([1], 2, [1], 1),
    ]

    for nums, target, expected_nums, expected_len in test_cases:
        original = nums.copy()
        result_len = yichu(nums, target)
        result_nums = nums[:result_len]
        
        passed = result_len == expected_len and sorted(result_nums) == sorted(expected_nums)
        status = "✅" if passed else "❌"
        
        print(f"{status} 原始: {original}")
        print(f"   目标: {target}")
        print(f"   结果: {nums} (前{result_len}个有效)")
        print(f"   预期: {expected_nums} (前{expected_len}个有效)")
        print()