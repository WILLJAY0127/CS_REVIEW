from typing import Optional, List, Tuple


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def build_linked_list(arr: List[int]) -> Optional[ListNode]:
    """数组 → 链表（独立链表，不共享节点）"""
    if not arr:
        return None
    head = ListNode(arr[0])
    cur = head
    for val in arr[1:]:
        cur.next = ListNode(val)
        cur = cur.next
    return head


def build_intersect_lists(
    arrA: List[int], arrB: List[int], arr_common: List[int]
) -> Tuple[Optional[ListNode], Optional[ListNode], Optional[ListNode]]:
    """
    构造 Y 形相交链表
    返回：(headA, headB, 交点 c1)
    """
    headA = build_linked_list(arrA)
    headB = build_linked_list(arrB)
    common = build_linked_list(arr_common)

    # A 的末尾接上公共段
    cur = headA
    if cur:
        while cur.next:
            cur = cur.next
        cur.next = common
    else:
        headA = common

    # B 的末尾接上公共段
    cur = headB
    if cur:
        while cur.next:
            cur = cur.next
        cur.next = common
    else:
        headB = common

    return headA, headB, common


def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    result = []
    cur = head
    while cur:
        result.append(cur.val)
        cur = cur.next
    return result


# ==================== 解法 1：长度对齐法 ====================
def getIntersectionNode_length_align(
    headA: Optional[ListNode], headB: Optional[ListNode]
) -> Optional[ListNode]:
    lenA, lenB = 0, 0
    cur = headA
    while cur:
        lenA += 1
        cur = cur.next
    cur = headB
    while cur:
        lenB += 1
        cur = cur.next

    pA, pB = headA, headB
    if lenB > lenA:
        gap = lenB - lenA
        for _ in range(gap):
            pB = pB.next
    else:
        gap = lenA - lenB
        for _ in range(gap):
            pA = pA.next

    while pA and pB:
        if pA is pB:
            return pA
        pA = pA.next
        pB = pB.next

    return None


# ==================== 解法 2：浪漫双指针 ====================
def getIntersectionNode_two_pointer(
    headA: Optional[ListNode], headB: Optional[ListNode]
) -> Optional[ListNode]:
    pA = headA
    pB = headB

    while pA != pB:
        pA = pA.next if pA else headB
        pB = pB.next if pB else headA

    return pA


# ==================== 解法 3：哈希集合 ====================
def getIntersectionNode_hash(
    headA: Optional[ListNode], headB: Optional[ListNode]
) -> Optional[ListNode]:
    seen = set()
    cur = headA
    while cur:
        seen.add(cur)
        cur = cur.next
    cur = headB
    while cur:
        if cur in seen:
            return cur
        cur = cur.next
    return None


if __name__ == "__main__":
    print("=" * 60)
    print("LeetCode 160 - 链表相交")
    print("=" * 60)

    # 构造测试用例：返回 (headA, headB, 预期交点对象或 None)
    def make_case(arrA, arrB, arr_common, intersect: bool):
        if intersect:
            return build_intersect_lists(arrA, arrB, arr_common)
        else:
            return build_linked_list(arrA), build_linked_list(arrB), None

    test_cases = []

    # case 1: 存在交点，arrA 短
    a1, b1, c1 = make_case(
        arrA=[4, 1],
        arrB=[5, 6, 1],
        arr_common=[8, 4, 5],
        intersect=True
    )
    test_cases.append(("有交点(A短B长)", a1, b1, c1, [8, 4, 5]))

    # case 2: 存在交点，arrB 短
    a2, b2, c2 = make_case(
        arrA=[1, 9, 1, 2],
        arrB=[3],
        arr_common=[4],
        intersect=True
    )
    test_cases.append(("有交点(A长B短)", a2, b2, c2, [4]))

    # case 3: 无交点
    a3, b3, c3 = make_case(
        arrA=[1, 2, 3],
        arrB=[4, 5],
        arr_common=[],
        intersect=False
    )
    test_cases.append(("无交点", a3, b3, None, []))

    # case 4: 一条链完全等于公共段（A 直接从 c1 开始）
    a4, b4, c4 = make_case(
        arrA=[],
        arrB=[1, 2, 3],
        arr_common=[7, 8, 9],
        intersect=True
    )
    test_cases.append(("A完全等于公共段", a4, b4, c4, [7, 8, 9]))

    # case 5: 两条链都空
    a5, b5, c5 = make_case(arrA=[], arrB=[], arr_common=[], intersect=False)
    test_cases.append(("两条都空", a5, b5, None, []))

    # case 6: 有交点且公共段就是最后单独一个节点
    a6, b6, c6 = make_case(
        arrA=[10, 20],
        arrB=[30, 40, 50],
        arr_common=[999],
        intersect=True
    )
    test_cases.append(("公共段单节点", a6, b6, c6, [999]))

    solutions = {
        "长度对齐法": getIntersectionNode_length_align,
        "浪漫双指针": getIntersectionNode_two_pointer,
        "哈希集合  ": getIntersectionNode_hash,
    }

    all_passed = True
    for sol_name, sol_func in solutions.items():
        print(f"\n📦 解法: {sol_name}")
        print("-" * 40)

        for case_name, headA, headB, expected_node, common_vals in test_cases:
            result_node = sol_func(headA, headB)

            # 交点必须是同一个对象！或者同时 None
            passed = (result_node is expected_node) or (
                result_node is None and expected_node is None
            )
            if not passed:
                all_passed = False

            status = "✅" if passed else "❌"
            res_vals = linked_list_to_list(result_node)
            print(f"  [{case_name}]")
            print(f"    A={linked_list_to_list(headA)}")
            print(f"    B={linked_list_to_list(headB)}")
            print(f"    公共段应={common_vals}")
            print(f"    从结果对象开始={res_vals}")
            print(f"    结果: {status}")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有解法全部通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 60)
