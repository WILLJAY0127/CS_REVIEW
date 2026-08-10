from typing import Optional, List, Tuple


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def build_linked_list(arr: List[int]) -> Optional[ListNode]:
    """数组 → 普通无环链表（独立节点）"""
    if not arr:
        return None
    head = ListNode(arr[0])
    cur = head
    for val in arr[1:]:
        cur.next = ListNode(val)
        cur = cur.next
    return head


def build_cycle_list(arr: List[int], pos: int) -> Tuple[Optional[ListNode], Optional[ListNode]]:
    """
    构造带环的链表
    pos: 入环点下标（从 0 开始，-1 表示无环）
    返回：(链表头, 入环点节点 or None)
    """
    head = build_linked_list(arr)
    if pos < 0 or not head:
        return head, None

    # 找到入环点节点
    entry = head
    for _ in range(pos):
        entry = entry.next

    # 找到尾巴，尾巴.next 接回入环点
    tail = head
    while tail.next:
        tail = tail.next
    tail.next = entry

    return head, entry


def linked_list_safe_to_list(head: Optional[ListNode], limit: int = 100) -> List[int]:
    """安全遍历（有环不会死循环），最多 limit 个节点"""
    result = []
    seen = set()
    cur = head
    while cur and cur not in seen and len(result) < limit:
        seen.add(cur)
        result.append(cur.val)
        cur = cur.next
    return result


# ==================== 解法 1：哈希集合暴力 ====================
def detectCycle_set(head: Optional[ListNode]) -> Optional[ListNode]:
    visited = set()
    cur = head
    while cur:
        if cur in visited:
            return cur
        visited.add(cur)
        cur = cur.next
    return None


# ==================== 解法 2：快慢指针（O(1) 空间） ====================
def detectCycle_floyd(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            p = head
            while p is not slow:
                p = p.next
                slow = slow.next
            return p
    return None


# ==================== 拓展：LC141 hasCycle（只判环不管入口） ====================
def hasCycle(head: Optional[ListNode]) -> bool:
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


if __name__ == "__main__":
    print("=" * 60)
    print("LeetCode 142 - 环形链表 II")
    print("=" * 60)

    # 构造测试：(描述, 链表构造函数返回 (head, 期望入口))
    def make(name, arr, pos):
        head, entry = build_cycle_list(arr, pos)
        return (name, head, entry, arr, pos)

    test_cases = [
        make("官方示例1 入环点pos=1", [3, 2, 0, -4], pos=1),
        make("官方示例2 从头就环 pos=0", [1, 2], pos=0),
        make("单节点自环 pos=0", [1], pos=0),
        make("长一点的环 pos=2", [10, 20, 30, 40, 50, 60], pos=2),
        make("无环 pos=-1", [1, 2, 3, 4], pos=-1),
        make("空链表 pos=-1", [], pos=-1),
        make("单节点无环 pos=-1", [1], pos=-1),
    ]

    solutions = {
        "哈希集合暴力": detectCycle_set,
        "快慢指针Floyd": detectCycle_floyd,
    }

    all_passed = True

    for sol_name, sol_func in solutions.items():
        print(f"\n📦 解法: {sol_name}")
        print("-" * 40)

        for name, head, expected_entry, arr, pos in test_cases:
            result_entry = sol_func(head)

            # 用 is 比较：必须是同一个对象，或同时 None
            passed = (result_entry is expected_entry) or (
                result_entry is None and expected_entry is None
            )
            if not passed:
                all_passed = False

            # 额外附加检查 LC141：hasCycle
            has_cycle_exp = pos >= 0
            has_cycle_res = hasCycle(head)
            lc141_ok = has_cycle_exp == has_cycle_res
            if not lc141_ok:
                all_passed = False

            status = "✅" if passed and lc141_ok else "❌"
            print(f"  [{name}]")
            print(f"    链表(最多看20个)={linked_list_safe_to_list(head, limit=20)}")
            print(f"    pos={pos}，期望入环点 val={expected_entry.val if expected_entry else None}")
            print(f"    实际返回 val={result_entry.val if result_entry else None}  "
                  f"| LC141环判定={has_cycle_res}(期望{has_cycle_exp})")
            print(f"    结果: {status}")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有解法 + LC141 全部通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 60)
