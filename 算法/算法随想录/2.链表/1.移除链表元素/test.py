from typing import Optional, List


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def list_to_linked_list(arr: List[int]) -> Optional[ListNode]:
    """将数组转换为链表"""
    if not arr:
        return None
    head = ListNode(arr[0])
    cur = head
    for val in arr[1:]:
        cur.next = ListNode(val)
        cur = cur.next
    return head


def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    """将链表转换为数组"""
    result = []
    cur = head
    while cur:
        result.append(cur.val)
        cur = cur.next
    return result


def removeElements_no_dummy(head: Optional[ListNode], val: int) -> Optional[ListNode]:
    """无 dummy 版本"""
    while head and head.val == val:
        head = head.next

    cur = head
    while cur and cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next
        else:
            cur = cur.next

    return head


def removeElements_with_dummy(head: Optional[ListNode], val: int) -> Optional[ListNode]:
    """有 dummy 版本（推荐）"""
    dummy = ListNode(val=0, next=head)
    cur = dummy

    while cur and cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next
        else:
            cur = cur.next

    return dummy.next


def removeElements_pre_cur(head: Optional[ListNode], val: int) -> Optional[ListNode]:
    """pre + cur 双指针版本"""
    pre = None
    cur = head

    while cur:
        if cur.val == val:
            if pre is None:
                head = cur.next
            else:
                pre.next = cur.next
        else:
            pre = cur
        cur = cur.next

    return head


if __name__ == "__main__":
    print("=" * 60)
    print("LeetCode 203 - 移除链表元素")
    print("=" * 60)

    test_cases = [
        ([1, 2, 6, 3, 4, 5, 6], 6, [1, 2, 3, 4, 5]),
        ([], 1, []),
        ([7, 7, 7, 7], 7, []),
        ([1, 1, 1, 1], 1, []),
        ([1, 2, 3, 4, 5], 6, [1, 2, 3, 4, 5]),
        ([1, 1, 2, 1, 1], 1, [2]),
        ([6, 1, 2, 6, 3], 6, [1, 2, 3]),
        ([1], 1, []),
        ([1], 2, [1]),
    ]

    solutions = {
        "no_dummy": removeElements_no_dummy,
        "with_dummy": removeElements_with_dummy,
        "pre_cur": removeElements_pre_cur,
    }

    all_passed = True

    for sol_name, sol_func in solutions.items():
        print(f"\n📦 解法: {sol_name}")
        print("-" * 40)

        for arr, val, expected in test_cases:
            head = list_to_linked_list(arr)
            result_head = sol_func(head, val)
            result = linked_list_to_list(result_head)

            passed = result == expected
            if not passed:
                all_passed = False

            status = "✅" if passed else "❌"
            print(f"  nums={arr}, val={val} → {result} {status}")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有解法全部通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 60)
