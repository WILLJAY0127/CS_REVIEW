def generateMatrix(n):
    res = [[0]*n for _ in range(n)]
    top, bottom = 0, n-1
    left, right = 0, n-1
    num = 1
    target = n * n

    while num <= target:
        # 左→右 上边框
        for i in range(left, right+1):
            res[top][i] = num
            num += 1
        top += 1

        # 上→下 右边框
        for i in range(top, bottom+1):
            res[i][right] = num
            num += 1
        right -= 1

        if top > bottom:
            break
        # 右→左 下边框
        for i in range(right, left-1, -1):
            res[bottom][i] = num
            num += 1
        bottom -= 1

        if left > right:
            break
        # 下→上 左边框
        for i in range(bottom, top-1, -1):
            res[i][left] = num
            num += 1
        left += 1
    return res