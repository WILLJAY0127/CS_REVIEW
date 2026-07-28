def minSubArrayLen_brute(target: int, nums: List[int]) -> int:
    n = len(nums)
    min_len = float('inf')

    for i in range(n):
        total = 0
        for j in range(i,n):
            total += nums[j]
            if total >= target:
                min_len = min(j-i+1,min_len)
                break

    return min_len if min_len != float('inf') else 0

def minSubArrayLen(target: int, nums: List[int]) -> int:

    return
