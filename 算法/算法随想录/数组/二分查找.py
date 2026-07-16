# class Solution:
#     def search(self, nums: List[int], target: int) -> int:    
#         return -1

# 二分查找 左闭右闭
class Solution:
    def search(self, nums: List[int], target: int) -> int:    
        left, right = 0, len(nums) -1

        while left <= right:
            mid = left + (right - left)//2

            if nums[mid] > target:
                right = mid - 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                return mid
        return -1


# 暴力循环
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # 暴力循环：逐个遍历每一个下标
        for i in range(len(nums)):
            if nums[i] == target:
                return i
        # 全部遍历完都没匹配，返回-1
        return -1        