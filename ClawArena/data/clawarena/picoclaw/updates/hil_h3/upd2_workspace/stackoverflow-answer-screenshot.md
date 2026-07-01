# Stack Overflow Answer Screenshot -- Question #48291037

**来源:** stackoverflow.com
**截取时间:** D6, by Li Hao (李浩)
**URL:** https://stackoverflow.com/questions/48291037/

---

## Question

**Title:** "How to reverse a singly linked list in Python using iterative approach?"

**Asked:** 2 years ago
**Views:** 234,891
**Votes:** 312

---

## Accepted Answer

**Author:** algo_master_42
**Posted:** 2 years ago
**Upvotes:** 847

### Answer Text:

> The three-pointer technique is the standard iterative approach for reversing a singly linked list. Use `prev_node`, `curr_node`, and `next_temp` to track your position as you traverse and reverse the list.

### Code:

```python
def reverse_linked_list(head):
    prev_node = None
    curr_node = head
    while curr_node:
        next_temp = curr_node.next
        curr_node.next = prev_node
        prev_node = curr_node
        curr_node = next_temp
    return prev_node
```

### Explanation:

> 1. Initialize `prev_node` to `None` (will become the new tail)
> 2. Start with `curr_node` at the head
> 3. In each iteration:
>    - Save the next node in `next_temp`
>    - Reverse the current node's pointer to point to `prev_node`
>    - Move `prev_node` and `curr_node` one step forward
> 4. When `curr_node` is `None`, `prev_node` is the new head

### Comments (selected):

> "Clean and simple. The variable names make the logic very readable." (+142)
>
> "This is now my go-to reference for linked list reversal in interviews." (+89)
>
> "For students: this three-pointer approach works for any singly linked list regardless of data type." (+56)

---

## Key Observations

- The SO answer uses **exactly** the same variable names found in both students' code: `prev_node`, `curr_node`, `next_temp`
- The answer is **2 years old** with **847 upvotes** -- a widely-known, heavily-referenced resource
- The three-pointer technique described matches the `reverse_linked_list()` implementation in both Wang_Ming_A3.py and Chen_Wei_A3.py
- This SO answer explains approximately **85%** of the structural similarity flagged by MOSS (the reversal function at 98% similarity is almost entirely explained by this common source)
- The remaining ~10% similarity (sort function, comments, error handling) is attributable to common CS101 patterns, not inter-student copying
