def yichu(nums:List[int], target: int) -> int:
    i = 0
    over = len(nums)


    while i < over:
        if target == nums[i]:
            for j in range(i+1, over):
                nums[j-1] = nums[j]
            over -= 1    
        else :
            i += 1
                
    return over