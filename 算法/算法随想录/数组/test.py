from typing import List

# 循环
def xunhuan(nums: List[int], target: int) -> int:
    for i in range(len(nums)):
        if target == nums[i]:
            return i
    return -1

# 二分


def erfen(nums: List[int], target: int) -> int:
    """
    二分查找【左闭右闭区间 [left, right]】
    前提：nums 升序有序数组
    :param nums: 有序数组
    :param target: 待查找目标
    :return: 目标下标，不存在返回 -1
    """
    left = 0
    right = len(nums) - 1
    print(f"【初始化】初始查找区间：下标范围 [{left}, {right}]")

    while left <= right:
        mid = left + (right - left) // 2
        print(f"\n【循环开始】当前区间 [{left}, {right}]，mid={mid}, nums[mid]={nums[mid]}")

        if target == nums[mid]:
            print(f"✅ 找到目标 target={target}，下标mid={mid}")
            return mid
        elif target > nums[mid]:
            print(f"🔍 target({target}) > nums[mid]({nums[mid]})，目标在右侧，更新 left = mid + 1 = {mid + 1}")
            left = mid + 1
        else:
            print(f"🔍 target({target}) < nums[mid]({nums[mid]})，目标在左侧，更新 right = mid - 1 = {mid - 1}")
            right = mid - 1
        print(f"【本轮结束】新区间 left={left}, right={right}")

    print(f"\n❌ 循环结束 left({left}) > right({right})，区间为空，未找到 target={target}")
    return -1


if __name__ == "__main__":
    test_cases = [
        # ([-1, 0, 3, 5, 9, 12], 9, 4)
        # ([-1, 0, 3, 5, 9, 12], 2, -1),
        # ([1, 3, 5], 1, 0),
        # ([1, 3, 5], 5, 2),
        # ([5], 5, 0),
        ([5], 3, -1)
    ]
    
    for nums, target, expected in test_cases:
        result = erfen(nums, target)
        status = "✅" if result == expected else "❌"
        print(f"{status} erfen({nums}, {target}) = {result} (expected: {expected})")

