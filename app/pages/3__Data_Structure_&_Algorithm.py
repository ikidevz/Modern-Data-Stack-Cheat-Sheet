import streamlit as st
from utility.seo import inject_seo
from components import sidebar

st.set_page_config(
    page_title="Data Structure & Algorithm - Modern Data Stack Cheat Sheet",
    page_icon="🧠",
    layout="wide",
)
inject_seo('DSA')

st.markdown("""
<style>
  .block-container { padding-top: 1.5rem; }
  .stTabs [data-baseweb="tab-list"] { gap: 8px; }
  .stTabs [data-baseweb="tab"] { padding: 6px 18px; border-radius: 6px; }
  code { font-size: 0.85em; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────

TOPICS = {
    "🏁 Big O Notation": {
        "tag": "Foundations",
        "complexity": {"Time": "varies", "Space": "varies"},
        "summary": (
            "**Big O Notation** describes the *worst-case* time or space complexity of an algorithm "
            "as a function of input size `n`. It focuses on **growth rate** rather than exact performance."
        ),
        "complexities": [
            ("O(1)", "Constant time — doesn't grow with input", "✅ Best"),
            ("O(log n)", "Logarithmic — halves the problem each step", "✅ Great"),
            ("O(n)", "Linear — scales proportionally with input", "🟡 OK"),
            ("O(n log n)", "Linearithmic — common in efficient sorts", "🟡 OK"),
            ("O(n²)", "Quadratic — nested loops over input", "🔴 Slow"),
            ("O(2ⁿ)", "Exponential — blows up fast", "🔴 Avoid"),
        ],
        "content": """
### What Is Big O?
Big O notation is the standard mathematical language to describe how an algorithm's **time** or **space**
requirements **grow** as `n` (input size) increases. It gives an **upper bound** — the worst case.
 
It ignores constants and lower-order terms:
- `O(5n²)` → `O(n²)`
- `O(n² + 2n + 1)` → `O(n²)`
 
### Time Complexity
Measures **how many operations** an algorithm does as input grows.
 
- A **single loop** → O(n)
- **Nested loops** → O(n²)
- **Halving** the problem each step → O(log n)
 
### Space Complexity
Measures **how much memory** an algorithm uses.
 
- Creating a new array of size n → O(n) space
- Modifying in-place (no new structures) → O(1) space
 
### Key Rule
Big O is about the **dominant term**. Drop constants, drop smaller terms.
""",
        "python_code": '''# O(1) - Constant
def get_first(arr):
    return arr[0]  # always 1 operation
 
# O(n) - Linear
def find_max(arr):
    max_val = arr[0]
    for x in arr:       # n operations
        if x > max_val:
            max_val = x
    return max_val
 
# O(n²) - Quadratic
def has_duplicate(arr):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):  # nested loop
            if arr[i] == arr[j]:
                return True
    return False
 
# O(log n) - Logarithmic
def binary_search(arr, target):
    L, R = 0, len(arr) - 1
    while L <= R:
        M = (L + R) // 2  # halves each time
        if arr[M] == target: return True
        elif arr[M] < target: L = M + 1
        else: R = M - 1
    return False''',
        "leetcode_examples": [
            {
                "id": "LC 1",
                "title": "Two Sum",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Given an array of integers, return indices of two numbers that add up to a target.",
                "approach": "HashMap approach: store each number and its index. For each number, check if complement exists in map.",
                "code": '''def twoSum(nums, target):
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
 
# Example
print(twoSum([2,7,11,15], 9))  # [0,1]
print(twoSum([3,2,4], 6))       # [1,2]'''
            },
            {
                "id": "LC 217",
                "title": "Contains Duplicate",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Return true if any value appears at least twice in the array.",
                "approach": "Add each element to a set. If element already in set → duplicate found.",
                "code": '''def containsDuplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
 
# Pythonic one-liner: O(n) time, O(n) space
def containsDuplicate2(nums):
    return len(nums) != len(set(nums))
 
print(containsDuplicate([1,2,3,1]))  # True
print(containsDuplicate([1,2,3,4]))  # False'''
            },
            {
                "id": "LC 242",
                "title": "Valid Anagram",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space (26 chars)",
                "description": "Given two strings s and t, return true if t is an anagram of s.",
                "approach": "Count character frequencies in both strings. Compare counts.",
                "code": '''from collections import Counter
 
def isAnagram(s, t):
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)
 
# Manual approach (shows the O(1) space trick)
def isAnagram2(s, t):
    count = [0] * 26
    for c in s: count[ord(c) - ord('a')] += 1
    for c in t: count[ord(c) - ord('a')] -= 1
    return all(x == 0 for x in count)
 
print(isAnagram("anagram", "nagaram"))  # True
print(isAnagram("rat", "car"))          # False'''
            },
            {
                "id": "LC 169",
                "title": "Majority Element",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space (Boyer-Moore)",
                "description": "Find the element that appears more than n/2 times.",
                "approach": "Boyer-Moore Voting: keep a candidate and count. When count hits 0, switch candidate.",
                "code": '''def majorityElement(nums):
    # Boyer-Moore Voting Algorithm: O(1) space!
    candidate, count = None, 0
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    return candidate
 
# Verify complexity: O(n) time, O(1) space
print(majorityElement([3,2,3]))        # 3
print(majorityElement([2,2,1,1,1,2,2])) # 2'''
            },
            {
                "id": "LC 268",
                "title": "Missing Number",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Find the missing number in range [0, n] given array of n distinct numbers.",
                "approach": "Expected sum of [0..n] = n*(n+1)//2. Subtract actual sum to get the missing number.",
                "code": '''def missingNumber(nums):
    n = len(nums)
    expected = n * (n + 1) // 2  # O(1) formula
    return expected - sum(nums)
 
# XOR approach: also O(n) time, O(1) space
def missingNumber2(nums):
    res = len(nums)
    for i, num in enumerate(nums):
        res ^= i ^ num  # XOR cancels pairs
    return res
 
print(missingNumber([3,0,1]))    # 2
print(missingNumber([9,6,4,2,3,5,7,0,1]))  # 8'''
            },
            {
                "id": "LC 412",
                "title": "FizzBuzz",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Return strings for 1..n: 'FizzBuzz' if div by 15, 'Fizz' if div by 3, 'Buzz' if div by 5.",
                "approach": "Iterate 1 to n, check divisibility with modulo. String concatenation trick avoids nested ifs.",
                "code": '''def fizzBuzz(n):
    result = []
    for i in range(1, n + 1):
        s = ""
        if i % 3 == 0: s += "Fizz"
        if i % 5 == 0: s += "Buzz"
        result.append(s or str(i))  # fallback to number
    return result
 
print(fizzBuzz(15))
# ['1','2','Fizz','4','Buzz','Fizz','7','8',
#  'Fizz','Buzz','11','Fizz','13','14','FizzBuzz']'''
            },
        ]
    },

    "📦 Arrays & Strings": {
        "tag": "Fundamentals",
        "complexity": {"Access": "O(1)", "Search": "O(n)", "Insert/Delete (mid)": "O(n)", "Append": "O(1) avg"},
        "summary": (
            "Arrays store elements in **contiguous memory**, giving O(1) index access. "
            "**Static arrays** are fixed-size; **dynamic arrays** (Python lists) resize automatically. "
            "Strings are immutable character arrays."
        ),
        "content": """
### Static Arrays
- **Fixed size** — can't grow after creation
- **O(1)** access by index (memory computed directly)
- **O(n)** insert/delete in the middle (need to shift elements)
 
### Dynamic Arrays (Python `list`)
Built on top of static arrays. When full, allocates a **new larger block** (usually 2x) and copies.
 
- **Append**: O(1) amortized — occasionally O(n) during resize
- **Insert at middle**: O(n) — must shift elements
- **Delete from end**: O(1)
- **Search**: O(n) unsorted
 
### Strings
In Python, strings are **immutable**. Every modification creates a **new string** — O(n) copy.
 
- Access character: O(1)
- Concatenation `s + 'z'`: O(n) — copies the whole string
- Length `len(s)`: O(1) — stored internally
""",
        "python_code": '''# Dynamic Arrays (Python lists)
A = [1, 2, 3]
A.append(5)          # O(1) amortized
A.pop()              # O(1) - remove last
A.insert(2, 5)       # O(n) - shift required
A[0] = 7             # O(1) - modify by index
print(A[2])          # O(1) - access by index
print(7 in A)        # O(n) - search
print(len(A))        # O(1)
 
# Strings
s = "hello"
print(s[2])          # O(1) - access
print(len(s))        # O(1)
b = s + "z"          # O(n) - creates new string
print("f" in s)      # O(n) - search''',
        "leetcode_examples": [
            {
                "id": "LC 121",
                "title": "Best Time to Buy and Sell Stock",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Find the maximum profit from one buy and one sell (buy before sell).",
                "approach": "Track the minimum price seen so far. At each price, compute profit vs current min. Update best profit.",
                "code": '''def maxProfit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit
 
print(maxProfit([7,1,5,3,6,4]))  # 5 (buy@1, sell@6)
print(maxProfit([7,6,4,3,1]))    # 0 (no profit possible)'''
            },
            {
                "id": "LC 238",
                "title": "Product of Array Except Self",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) extra space",
                "description": "Return array where output[i] = product of all elements except nums[i]. No division allowed.",
                "approach": "Two passes: first pass builds prefix products, second pass multiplies suffix products into result.",
                "code": '''def productExceptSelf(nums):
    n = len(nums)
    result = [1] * n
 
    # Left pass: result[i] = product of all elements left of i
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
 
    # Right pass: multiply in product of all elements right of i
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
 
    return result
 
print(productExceptSelf([1,2,3,4]))   # [24,12,8,6]
print(productExceptSelf([-1,1,0,-3,3])) # [0,0,9,0,0]'''
            },
            {
                "id": "LC 53",
                "title": "Maximum Subarray",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Find the contiguous subarray with the largest sum (Kadane's Algorithm).",
                "approach": "Kadane's: track current running sum. If it goes negative, reset to 0 (start fresh). Track global max.",
                "code": '''def maxSubArray(nums):
    max_sum = nums[0]
    curr_sum = 0
    for num in nums:
        curr_sum = max(num, curr_sum + num)  # restart if negative
        max_sum = max(max_sum, curr_sum)
    return max_sum
 
print(maxSubArray([-2,1,-3,4,-1,2,1,-5,4]))  # 6 (subarray [4,-1,2,1])
print(maxSubArray([1]))                        # 1
print(maxSubArray([5,4,-1,7,8]))              # 23'''
            },
            {
                "id": "LC 56",
                "title": "Merge Intervals",
                "difficulty": "Medium",
                "complexity": "O(n log n) time, O(n) space",
                "description": "Merge all overlapping intervals and return the resulting list.",
                "approach": "Sort by start time. Iterate: if current start <= last merged end, extend the end. Otherwise add new interval.",
                "code": '''def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
 
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:       # overlapping
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])  # no overlap, add new
 
    return merged
 
print(merge([[1,3],[2,6],[8,10],[15,18]]))
# [[1,6],[8,10],[15,18]]
print(merge([[1,4],[4,5]]))
# [[1,5]]'''
            },
            {
                "id": "LC 152",
                "title": "Maximum Product Subarray",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Find the contiguous subarray that has the largest product.",
                "approach": "Track both max and min products (negatives can flip). At each step update both, then update global max.",
                "code": '''def maxProduct(nums):
    res = max(nums)
    cur_min, cur_max = 1, 1
 
    for num in nums:
        if num == 0:
            cur_min, cur_max = 1, 1
            continue
        candidates = (num, cur_max * num, cur_min * num)
        cur_max = max(candidates)
        cur_min = min(candidates)
        res = max(res, cur_max)
 
    return res
 
print(maxProduct([2,3,-2,4]))  # 6 (subarray [2,3])
print(maxProduct([-2,0,-1]))   # 0'''
            },
            {
                "id": "LC 128",
                "title": "Longest Consecutive Sequence",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "Find the length of the longest consecutive sequence in an unsorted array.",
                "approach": "Use a HashSet. Only start counting from a number with no left neighbor (n-1 not in set). Count streak from there.",
                "code": '''def longestConsecutive(nums):
    num_set = set(nums)
    best = 0
 
    for n in num_set:
        if n - 1 not in num_set:  # only start from sequence beginning
            length = 1
            while n + length in num_set:
                length += 1
            best = max(best, length)
 
    return best
 
print(longestConsecutive([100,4,200,1,3,2]))  # 4 (1,2,3,4)
print(longestConsecutive([0,3,7,2,5,8,4,6,0,1]))  # 9'''
            },
            {
                "id": "LC 11",
                "title": "Container With Most Water",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Find two lines that form a container holding the most water.",
                "approach": "Two pointers from both ends. Area = min(height[L], height[R]) * (R - L). Move the shorter side inward.",
                "code": '''def maxArea(height):
    L, R = 0, len(height) - 1
    max_water = 0
 
    while L < R:
        water = min(height[L], height[R]) * (R - L)
        max_water = max(max_water, water)
        if height[L] < height[R]:
            L += 1  # move shorter side
        else:
            R -= 1
    return max_water
 
print(maxArea([1,8,6,2,5,4,8,3,7]))  # 49
print(maxArea([1,1]))                  # 1'''
            },
        ]
    },

    "🗺️ Hashmaps & Sets": {
        "tag": "Fundamentals",
        "complexity": {"Insert": "O(1) avg", "Delete": "O(1) avg", "Lookup": "O(1) avg", "Worst case": "O(n)"},
        "summary": (
            "Hash tables map **keys → values** using a hash function. "
            "**HashSets** store unique elements. **HashMaps** store key-value pairs. "
            "Average O(1) for insert, delete, lookup."
        ),
        "content": """
### How Hashing Works
A **hash function** converts a key into an array index using modulo arithmetic.
**Collisions** (two keys → same index) are resolved by:
- **Separate chaining**: linked list at each bucket
- **Linear probing**: find next empty slot
 
### HashSet
- Stores **unique** elements only
- O(1) membership test: `x in s`
- Keys must be **hashable** (immutable) — strings, ints, tuples ✅; lists ❌
 
### HashMap (dict)
- Stores **key → value** pairs
- O(1) insert, lookup, delete
- Python's `dict` and `set` are built-in hash tables
 
### Useful Python Tools
- `dict` / `set` — standard hash structures
- `collections.defaultdict` — default value for missing keys
- `collections.Counter` — frequency counting shortcut
""",
        "python_code": '''from collections import defaultdict, Counter
 
# HashSet
s = set()
s.add(1); s.add(2); s.add(3)
print(1 in s)        # O(1) lookup
s.remove(3)          # O(1) delete
 
# From a string — get unique chars
unique = set("aaabbbccc")   # {'a','b','c'}
 
# HashMap (dict)
d = {"greg": 1, "steve": 2}
d["arsh"] = 4        # O(1) insert
print("greg" in d)   # O(1) key check
print(d["greg"])     # O(1) value lookup
for k, v in d.items():  # O(n) iteration
    print(k, v)
 
# defaultdict — no KeyError on missing key
freq = defaultdict(int)
for c in "banana":
    freq[c] += 1
 
# Counter — frequency counting
counts = Counter("banana")
# Counter({'a': 3, 'n': 2, 'b': 1})''',
        "leetcode_examples": [
            {
                "id": "LC 49",
                "title": "Group Anagrams",
                "difficulty": "Medium",
                "complexity": "O(n * k) time, O(n * k) space",
                "description": "Group strings that are anagrams of each other.",
                "approach": "Use sorted string as key in hashmap. All anagrams produce the same sorted key.",
                "code": '''from collections import defaultdict
 
def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # "eat","tea","ate" → ('a','e','t')
        groups[key].append(s)
    return list(groups.values())
 
print(groupAnagrams(["eat","tea","tan","ate","nat","bat"]))
# [['eat','tea','ate'], ['tan','nat'], ['bat']]'''
            },
            {
                "id": "LC 347",
                "title": "Top K Frequent Elements",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space (bucket sort)",
                "description": "Return the k most frequent elements from the array.",
                "approach": "Count frequencies, then bucket sort by frequency index. Collect from end of bucket array.",
                "code": '''def topKFrequent(nums, k):
    count = {}
    freq = [[] for _ in range(len(nums) + 1)]
 
    for n in nums:
        count[n] = 1 + count.get(n, 0)
    for n, c in count.items():
        freq[c].append(n)
 
    res = []
    for i in range(len(freq) - 1, 0, -1):
        for n in freq[i]:
            res.append(n)
            if len(res) == k:
                return res
 
print(topKFrequent([1,1,1,2,2,3], 2))  # [1,2]
print(topKFrequent([1], 1))             # [1]'''
            },
            {
                "id": "LC 128",
                "title": "Longest Consecutive Sequence",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "Find the length of the longest consecutive sequence in an unsorted array.",
                "approach": "Store all numbers in a set. For each number, check if it's the start of a sequence (n-1 not in set). Count forward.",
                "code": '''def longestConsecutive(nums):
    num_set = set(nums)
    best = 0
 
    for n in num_set:
        if n - 1 not in num_set:  # start of sequence
            cur = n
            streak = 1
            while cur + 1 in num_set:
                cur += 1
                streak += 1
            best = max(best, streak)
 
    return best
 
print(longestConsecutive([100,4,200,1,3,2]))  # 4'''
            },
            {
                "id": "LC 560",
                "title": "Subarray Sum Equals K",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "Count the number of subarrays that sum to k.",
                "approach": "Prefix sum + hashmap. If prefix_sum - k exists in map, we found a valid subarray.",
                "code": '''def subarraySum(nums, k):
    count = 0
    prefix = 0
    seen = {0: 1}  # prefix_sum -> frequency
 
    for num in nums:
        prefix += num
        if prefix - k in seen:
            count += seen[prefix - k]
        seen[prefix] = seen.get(prefix, 0) + 1
 
    return count
 
print(subarraySum([1,1,1], 2))    # 2
print(subarraySum([1,2,3], 3))    # 2'''
            },
            {
                "id": "LC 290",
                "title": "Word Pattern",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Check if a string follows the same pattern as given pattern string.",
                "approach": "Two-way bijection: map pattern chars to words AND words to pattern chars. Both must match.",
                "code": '''def wordPattern(pattern, s):
    words = s.split()
    if len(pattern) != len(words):
        return False
 
    char_to_word = {}
    word_to_char = {}
 
    for c, w in zip(pattern, words):
        if c in char_to_word and char_to_word[c] != w:
            return False
        if w in word_to_char and word_to_char[w] != c:
            return False
        char_to_word[c] = w
        word_to_char[w] = c
 
    return True
 
print(wordPattern("abba", "dog cat cat dog"))  # True
print(wordPattern("abba", "dog cat cat fish"))  # False'''
            },
            {
                "id": "LC 451",
                "title": "Sort Characters By Frequency",
                "difficulty": "Medium",
                "complexity": "O(n log n) time, O(n) space",
                "description": "Sort characters in a string by decreasing frequency.",
                "approach": "Count frequencies with Counter, then sort by frequency descending and build result string.",
                "code": '''from collections import Counter
 
def frequencySort(s):
    freq = Counter(s)
    # Sort by frequency descending, build string
    return ''.join(char * count
                   for char, count in freq.most_common())
 
print(frequencySort("tree"))   # "eert" or "eetr"
print(frequencySort("cccaaa")) # "cccaaa" or "aaaccc"
print(frequencySort("Aabb"))   # "bbAa" or "bbaA"'''
            },
            {
                "id": "LC 205",
                "title": "Isomorphic Strings",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Determine if two strings are isomorphic (same structure mapping).",
                "approach": "Map each char in s to char in t, and vice versa. Check consistency of both mappings.",
                "code": '''def isIsomorphic(s, t):
    s_to_t = {}
    t_to_s = {}
 
    for cs, ct in zip(s, t):
        if cs in s_to_t and s_to_t[cs] != ct:
            return False
        if ct in t_to_s and t_to_s[ct] != cs:
            return False
        s_to_t[cs] = ct
        t_to_s[ct] = cs
 
    return True
 
print(isIsomorphic("egg", "add"))   # True
print(isIsomorphic("foo", "bar"))   # False
print(isIsomorphic("paper", "title"))  # True'''
            },
        ]
    },

    "👆 2 Pointers": {
        "tag": "Technique",
        "complexity": {"Time": "O(n)", "Space": "O(1)"},
        "summary": (
            "Use **two indices** that move toward or away from each other to solve array/string problems "
            "in O(n) instead of O(n²) with nested loops."
        ),
        "content": """
### The Squeeze Pattern
One pointer at the **start**, one at the **end**. Move them **inward** based on conditions.
 
Use when:
- Array is **sorted** and you need pairs
- Checking **palindromes**
- Comparing from **both ends**
 
### Same-Direction Pattern
Both pointers move **forward** — a fast pointer and a slow pointer.
 
Use when:
- Removing duplicates
- Finding the middle of a linked list
- Cycle detection
 
### Why It Works
At each step you eliminate part of the search space. You never need to re-examine eliminated elements → **O(n) total**.
""",
        "python_code": '''# Squeeze: find pair summing to target in sorted array
def two_sum_sorted(arr, target):
    L, R = 0, len(arr) - 1
    while L < R:
        total = arr[L] + arr[R]
        if total == target:
            return [L, R]
        elif total < target:
            L += 1   # need bigger sum
        else:
            R -= 1   # need smaller sum
    return []
 
# Palindrome check
def is_palindrome(s):
    L, R = 0, len(s) - 1
    while L < R:
        if s[L] != s[R]:
            return False
        L += 1; R -= 1
    return True''',
        "leetcode_examples": [
            {
                "id": "LC 15",
                "title": "3Sum",
                "difficulty": "Medium",
                "complexity": "O(n²) time, O(1) space",
                "description": "Find all unique triplets in array that sum to zero.",
                "approach": "Sort array. For each element, use two pointers on remaining. Skip duplicates carefully.",
                "code": '''def threeSum(nums):
    nums.sort()
    res = []
 
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue  # skip duplicate
        L, R = i + 1, len(nums) - 1
        while L < R:
            total = nums[i] + nums[L] + nums[R]
            if total == 0:
                res.append([nums[i], nums[L], nums[R]])
                while L < R and nums[L] == nums[L+1]: L += 1
                while L < R and nums[R] == nums[R-1]: R -= 1
                L += 1; R -= 1
            elif total < 0:
                L += 1
            else:
                R -= 1
 
    return res
 
print(threeSum([-1,0,1,2,-1,-4]))
# [[-1,-1,2],[-1,0,1]]'''
            },
            {
                "id": "LC 125",
                "title": "Valid Palindrome",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Check if a string is a palindrome considering only alphanumeric characters.",
                "approach": "Two pointers from both ends, skip non-alphanumeric, compare chars (case-insensitive).",
                "code": '''def isPalindrome(s):
    L, R = 0, len(s) - 1
 
    while L < R:
        while L < R and not s[L].isalnum():
            L += 1
        while L < R and not s[R].isalnum():
            R -= 1
        if s[L].lower() != s[R].lower():
            return False
        L += 1; R -= 1
 
    return True
 
print(isPalindrome("A man, a plan, a canal: Panama"))  # True
print(isPalindrome("race a car"))                       # False
print(isPalindrome(" "))                                # True'''
            },
            {
                "id": "LC 167",
                "title": "Two Sum II - Input Array Is Sorted",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Find two numbers in a sorted array that add up to target. Return 1-indexed positions.",
                "approach": "Classic squeeze pattern: L at start, R at end. Move based on sum vs target.",
                "code": '''def twoSum(numbers, target):
    L, R = 0, len(numbers) - 1
 
    while L < R:
        total = numbers[L] + numbers[R]
        if total == target:
            return [L + 1, R + 1]  # 1-indexed
        elif total < target:
            L += 1
        else:
            R -= 1
 
    return []
 
print(twoSum([2,7,11,15], 9))   # [1,2]
print(twoSum([2,3,4], 6))        # [1,3]'''
            },
            {
                "id": "LC 26",
                "title": "Remove Duplicates from Sorted Array",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Remove duplicates in-place from sorted array. Return new length.",
                "approach": "Slow pointer tracks position for next unique. Fast pointer scans ahead for new unique values.",
                "code": '''def removeDuplicates(nums):
    slow = 1  # position for next unique element
 
    for fast in range(1, len(nums)):
        if nums[fast] != nums[fast - 1]:
            nums[slow] = nums[fast]
            slow += 1
 
    return slow
 
nums = [1,1,2]
k = removeDuplicates(nums)
print(k, nums[:k])  # 2 [1, 2]
 
nums = [0,0,1,1,1,2,2,3,3,4]
k = removeDuplicates(nums)
print(k, nums[:k])  # 5 [0, 1, 2, 3, 4]'''
            },
            {
                "id": "LC 977",
                "title": "Squares of a Sorted Array",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Return sorted squares of each number in sorted array.",
                "approach": "Two pointers from both ends. Largest square is at one of the ends. Fill result array from right to left.",
                "code": '''def sortedSquares(nums):
    L, R = 0, len(nums) - 1
    result = [0] * len(nums)
    pos = len(nums) - 1  # fill from right
 
    while L <= R:
        if abs(nums[L]) > abs(nums[R]):
            result[pos] = nums[L] ** 2
            L += 1
        else:
            result[pos] = nums[R] ** 2
            R -= 1
        pos -= 1
 
    return result
 
print(sortedSquares([-4,-1,0,3,10]))  # [0,1,9,16,100]
print(sortedSquares([-7,-3,2,3,11]))  # [4,9,9,49,121]'''
            },
            {
                "id": "LC 42",
                "title": "Trapping Rain Water",
                "difficulty": "Hard",
                "complexity": "O(n) time, O(1) space",
                "description": "Calculate how much water can be trapped between heights.",
                "approach": "Two pointers. Track max height seen from left and right. Water at position = min(maxL, maxR) - height.",
                "code": '''def trap(height):
    L, R = 0, len(height) - 1
    maxL, maxR = height[L], height[R]
    water = 0
 
    while L < R:
        if maxL <= maxR:
            L += 1
            maxL = max(maxL, height[L])
            water += maxL - height[L]
        else:
            R -= 1
            maxR = max(maxR, height[R])
            water += maxR - height[R]
 
    return water
 
print(trap([0,1,0,2,1,0,1,3,2,1,2,1]))  # 6
print(trap([4,2,0,3,2,5]))               # 9'''
            },
            {
                "id": "LC 80",
                "title": "Remove Duplicates from Sorted Array II",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Allow each unique element to appear at most twice. Return new length.",
                "approach": "Slow pointer at index 2. For each element, compare with nums[slow-2]. If different, keep it.",
                "code": '''def removeDuplicates(nums):
    slow = 2  # first 2 elements always valid
 
    for fast in range(2, len(nums)):
        if nums[fast] != nums[slow - 2]:
            nums[slow] = nums[fast]
            slow += 1
 
    return slow
 
nums = [1,1,1,2,2,3]
k = removeDuplicates(nums)
print(k, nums[:k])  # 5 [1,1,2,2,3]'''
            },
        ]
    },

    "📚 Stacks & Queues": {
        "tag": "Fundamentals",
        "complexity": {"Push/Pop (Stack)": "O(1)", "Enqueue/Dequeue (Queue)": "O(1)", "Peek": "O(1)"},
        "summary": (
            "**Stacks** are Last-In-First-Out (LIFO). **Queues** are First-In-First-Out (FIFO). "
            "Both support O(1) insert and remove from their designated end."
        ),
        "content": """
### Stack (LIFO)
Like a stack of plates — **last placed, first removed**.
 
Operations:
- `push` / `append` — add to top: O(1)
- `pop` — remove from top: O(1)
- `peek` / `[-1]` — view top: O(1)
 
Python: use a `list` (append/pop from end)
 
### Queue (FIFO)
Like a line at a store — **first in, first out**.
 
Operations:
- `enqueue` / `append` — add to back: O(1)
- `dequeue` / `popleft` — remove from front: O(1)
 
⚠️ Don't use `list.pop(0)` — it's O(n)! Use `collections.deque` instead.
 
### Real-World Uses
| Stack | Queue |
|-------|-------|
| Browser back button | Print job queue |
| Undo/redo | BFS graph traversal |
| Call stack | Task scheduling |
| Balanced parentheses | Buffering |
""",
        "python_code": '''from collections import deque
 
# Stack using list
stack = []
stack.append(5)   # push O(1)
stack.append(4)
stack.append(3)
top = stack[-1]   # peek O(1)  → 3
x = stack.pop()   # pop O(1)   → 3
 
# Queue using deque (O(1) on both ends)
q = deque()
q.append(5)       # enqueue O(1)
q.append(6)
item = q.popleft()  # dequeue O(1) → 5''',
        "leetcode_examples": [
            {
                "id": "LC 20",
                "title": "Valid Parentheses",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Determine if a string of brackets is valid (properly opened and closed).",
                "approach": "Push open brackets onto stack. On close bracket, check if top of stack matches. Stack must be empty at end.",
                "code": '''def isValid(s):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
 
    for ch in s:
        if ch in "({[":
            stack.append(ch)
        else:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
 
    return len(stack) == 0
 
print(isValid("()"))      # True
print(isValid("()[]{}"))  # True
print(isValid("(]"))      # False
print(isValid("([)]"))    # False'''
            },
            {
                "id": "LC 155",
                "title": "Min Stack",
                "difficulty": "Medium",
                "complexity": "O(1) all operations",
                "description": "Design a stack that supports push, pop, top, and retrieving the minimum element in O(1).",
                "approach": "Use two stacks: one normal, one tracking minimums. Push to min_stack only when new min found.",
                "code": '''class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # tracks minimums
 
    def push(self, val):
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)
 
    def pop(self):
        self.stack.pop()
        self.min_stack.pop()
 
    def top(self):
        return self.stack[-1]
 
    def getMin(self):
        return self.min_stack[-1]
 
ms = MinStack()
ms.push(-2); ms.push(0); ms.push(-3)
print(ms.getMin())  # -3
ms.pop()
print(ms.top())     # 0
print(ms.getMin())  # -2'''
            },
            {
                "id": "LC 739",
                "title": "Daily Temperatures",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "For each day, find how many days until a warmer temperature. Return 0 if no warmer day.",
                "approach": "Monotonic stack storing indices. When we find a warmer day, pop and compute difference in indices.",
                "code": '''def dailyTemperatures(temperatures):
    n = len(temperatures)
    result = [0] * n
    stack = []  # stores indices, decreasing temps
 
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
 
    return result
 
print(dailyTemperatures([73,74,75,71,69,72,76,73]))
# [1, 1, 4, 2, 1, 1, 0, 0]'''
            },
            {
                "id": "LC 84",
                "title": "Largest Rectangle in Histogram",
                "difficulty": "Hard",
                "complexity": "O(n) time, O(n) space",
                "description": "Find the largest rectangle area in a histogram.",
                "approach": "Monotonic stack (increasing). When we see shorter bar, pop and calculate area extending left.",
                "code": '''def largestRectangleArea(heights):
    stack = []   # (index, height)
    max_area = 0
 
    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx  # can extend back to this index
        stack.append((start, h))
 
    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))
 
    return max_area
 
print(largestRectangleArea([2,1,5,6,2,3]))  # 10
print(largestRectangleArea([2,4]))           # 4'''
            },
            {
                "id": "LC 232",
                "title": "Implement Queue using Stacks",
                "difficulty": "Easy",
                "complexity": "O(1) amortized push/pop",
                "description": "Implement a FIFO queue using only two stacks.",
                "approach": "Two stacks: inbox for push, outbox for pop. Transfer inbox→outbox lazily when outbox is empty.",
                "code": '''class MyQueue:
    def __init__(self):
        self.inbox = []   # for push
        self.outbox = []  # for pop/peek
 
    def push(self, x):
        self.inbox.append(x)
 
    def _transfer(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
 
    def pop(self):
        self._transfer()
        return self.outbox.pop()
 
    def peek(self):
        self._transfer()
        return self.outbox[-1]
 
    def empty(self):
        return not self.inbox and not self.outbox
 
q = MyQueue()
q.push(1); q.push(2)
print(q.peek())  # 1
print(q.pop())   # 1
print(q.empty()) # False'''
            },
            {
                "id": "LC 150",
                "title": "Evaluate Reverse Polish Notation",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "Evaluate the value of an arithmetic expression in Reverse Polish Notation.",
                "approach": "Push numbers onto stack. On operator, pop two numbers, apply operator, push result.",
                "code": '''def evalRPN(tokens):
    stack = []
    ops = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b),  # truncate toward zero
    }
 
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
 
    return stack[0]
 
print(evalRPN(["2","1","+","3","*"]))        # 9
print(evalRPN(["4","13","5","/","+"]))        # 6
print(evalRPN(["10","6","9","3","+","-11","*","/","*","17","+","5","+"]))  # 22'''
            },
        ]
    },

    "🔗 Linked Lists": {
        "tag": "Fundamentals",
        "complexity": {"Insert at head/tail": "O(1)", "Search": "O(n)", "Insert/Delete at pos": "O(n)"},
        "summary": (
            "Nodes connected by **pointers** — not contiguous memory. "
            "**Singly** linked lists traverse one direction; **Doubly** linked allow bidirectional travel."
        ),
        "content": """
### Singly Linked List
Each node holds: `value` + `next` pointer.
 
- Insert at **head**: O(1)
- Search: O(n) — must traverse from head
- Delete: O(n) — need previous node reference
 
### Doubly Linked List
Each node holds: `prev` + `value` + `next`.
 
- Insert at head **and** tail: O(1)
- Delete with reference: O(1) — knows both neighbors
 
### Linked List vs Array
| Feature | Array | Linked List |
|---------|-------|-------------|
| Access by index | O(1) | O(n) |
| Insert at front | O(n) | O(1) |
| Memory | Contiguous | Scattered |
""",
        "python_code": '''class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next
 
# Reverse linked list
def reverse(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev  # new head''',
        "leetcode_examples": [
            {
                "id": "LC 206",
                "title": "Reverse Linked List",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Reverse a singly linked list.",
                "approach": "Iteratively re-point each node's next to its previous node. Three pointers: prev, curr, next.",
                "code": '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val; self.next = next
 
def reverseList(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next   # save next
        curr.next = prev  # reverse pointer
        prev = curr       # advance prev
        curr = nxt        # advance curr
    return prev  # new head
 
# Recursive version
def reverseList2(head):
    if not head or not head.next:
        return head
    new_head = reverseList2(head.next)
    head.next.next = head
    head.next = None
    return new_head'''
            },
            {
                "id": "LC 21",
                "title": "Merge Two Sorted Lists",
                "difficulty": "Easy",
                "complexity": "O(m+n) time, O(1) space",
                "description": "Merge two sorted linked lists and return one sorted list.",
                "approach": "Use a dummy head. Compare heads of both lists, attach smaller one, advance that pointer.",
                "code": '''def mergeTwoLists(l1, l2):
    dummy = ListNode(0)
    curr = dummy
 
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
 
    curr.next = l1 or l2  # attach remaining
 
    return dummy.next'''
            },
            {
                "id": "LC 141",
                "title": "Linked List Cycle",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Detect if a linked list has a cycle.",
                "approach": "Floyd's Tortoise and Hare: slow moves 1 step, fast moves 2 steps. If there's a cycle, they meet.",
                "code": '''def hasCycle(head):
    slow = fast = head
 
    while fast and fast.next:
        slow = slow.next        # 1 step
        fast = fast.next.next   # 2 steps
        if slow is fast:
            return True  # cycle detected!
 
    return False'''
            },
            {
                "id": "LC 143",
                "title": "Reorder List",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Reorder list: L0→L1→…→Ln becomes L0→Ln→L1→Ln-1→L2→Ln-2→…",
                "approach": "1) Find middle (slow/fast pointers), 2) Reverse second half, 3) Merge two halves.",
                "code": '''def reorderList(head):
    # Step 1: find middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
 
    # Step 2: reverse second half
    second = slow.next
    slow.next = None  # split
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
    second = prev
 
    # Step 3: merge
    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2'''
            },
            {
                "id": "LC 19",
                "title": "Remove Nth Node From End of List",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Remove the nth node from the end of a linked list in one pass.",
                "approach": "Two pointers: advance fast n steps ahead. Then move both until fast reaches end. Slow is at target.",
                "code": '''def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    slow, fast = dummy, dummy
 
    # Move fast n+1 steps ahead
    for _ in range(n + 1):
        fast = fast.next
 
    # Move both until fast reaches end
    while fast:
        slow = slow.next
        fast = fast.next
 
    # Remove nth from end
    slow.next = slow.next.next
    return dummy.next'''
            },
            {
                "id": "LC 2",
                "title": "Add Two Numbers",
                "difficulty": "Medium",
                "complexity": "O(max(m,n)) time, O(max(m,n)) space",
                "description": "Add two numbers stored in reverse order as linked lists. Return sum as linked list.",
                "approach": "Simulate addition digit by digit with carry. Process both lists simultaneously.",
                "code": '''def addTwoNumbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0
 
    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
 
        total = v1 + v2 + carry
        carry = total // 10
        curr.next = ListNode(total % 10)
 
        curr = curr.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next
 
    return dummy.next'''
            },
            {
                "id": "LC 287",
                "title": "Find the Duplicate Number",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Find the duplicate in array of n+1 integers in range [1,n]. Can't modify array.",
                "approach": "Floyd's cycle detection — treat array values as pointers. Find cycle entry = duplicate.",
                "code": '''def findDuplicate(nums):
    # Phase 1: detect cycle
    slow = fast = 0
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
 
    # Phase 2: find cycle entry
    slow2 = 0
    while slow != slow2:
        slow = nums[slow]
        slow2 = nums[slow2]
 
    return slow
 
print(findDuplicate([1,3,4,2,2]))  # 2
print(findDuplicate([3,1,3,4,2]))  # 3'''
            },
        ]
    },

    "🔍 Binary Search": {
        "tag": "Technique",
        "complexity": {"Time": "O(log n)", "Space": "O(1)"},
        "summary": (
            "Efficiently find a target in a **sorted** array by repeatedly **halving** the search range. "
            "O(log n) — much faster than O(n) linear search."
        ),
        "content": """
### Traditional Binary Search
Find if a **specific value** exists in a sorted array.
 
1. `L = 0`, `R = n-1`
2. Loop while `L <= R`
3. `M = (L + R) // 2`
4. If `arr[M] == target` → found!
5. If `arr[M] < target` → `L = M + 1`
6. If `arr[M] > target` → `R = M - 1`
 
### Condition-Based Binary Search
Find the **first index** where a condition becomes True.
 
1. `L = 0`, `R = n-1`
2. Loop while `L < R` (strict)
3. If condition at M is True → `R = M`
4. If False → `L = M + 1`
5. Return `L` — the boundary
""",
        "python_code": '''def binary_search(arr, target):
    L, R = 0, len(arr) - 1
    while L <= R:
        M = (L + R) // 2
        if arr[M] == target: return True
        elif arr[M] < target: L = M + 1
        else: R = M - 1
    return False''',
        "leetcode_examples": [
            {
                "id": "LC 704",
                "title": "Binary Search",
                "difficulty": "Easy",
                "complexity": "O(log n) time, O(1) space",
                "description": "Search for a target in a sorted array. Return its index or -1.",
                "approach": "Standard binary search: compare target with middle element, narrow search range.",
                "code": '''def search(nums, target):
    L, R = 0, len(nums) - 1
 
    while L <= R:
        M = (L + R) // 2
        if nums[M] == target:
            return M
        elif nums[M] < target:
            L = M + 1
        else:
            R = M - 1
 
    return -1
 
print(search([-1,0,3,5,9,12], 9))   # 4
print(search([-1,0,3,5,9,12], 2))   # -1'''
            },
            {
                "id": "LC 74",
                "title": "Search a 2D Matrix",
                "difficulty": "Medium",
                "complexity": "O(log(m*n)) time, O(1) space",
                "description": "Search for target in m×n matrix where each row is sorted and first element of each row > last of previous row.",
                "approach": "Treat the matrix as a flattened sorted array. Binary search on virtual index, convert to row/col.",
                "code": '''def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    L, R = 0, m * n - 1
 
    while L <= R:
        M = (L + R) // 2
        row, col = M // n, M % n  # convert flat → 2D
        val = matrix[row][col]
 
        if val == target:
            return True
        elif val < target:
            L = M + 1
        else:
            R = M - 1
 
    return False
 
print(searchMatrix([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 3))   # True
print(searchMatrix([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 13))  # False'''
            },
            {
                "id": "LC 153",
                "title": "Find Minimum in Rotated Sorted Array",
                "difficulty": "Medium",
                "complexity": "O(log n) time, O(1) space",
                "description": "Find the minimum element in a rotated sorted array with no duplicates.",
                "approach": "If mid > right, minimum is in right half. Otherwise it's in left half (including mid).",
                "code": '''def findMin(nums):
    L, R = 0, len(nums) - 1
 
    while L < R:
        M = (L + R) // 2
        if nums[M] > nums[R]:
            L = M + 1  # min is in right half
        else:
            R = M      # min is in left half (or at M)
 
    return nums[L]
 
print(findMin([3,4,5,1,2]))    # 1
print(findMin([4,5,6,7,0,1,2])) # 0
print(findMin([11,13,15,17]))   # 11'''
            },
            {
                "id": "LC 33",
                "title": "Search in Rotated Sorted Array",
                "difficulty": "Medium",
                "complexity": "O(log n) time, O(1) space",
                "description": "Search for target in a rotated sorted array.",
                "approach": "Determine which half is sorted. If target in sorted half, go there; else go to other half.",
                "code": '''def search(nums, target):
    L, R = 0, len(nums) - 1
 
    while L <= R:
        M = (L + R) // 2
        if nums[M] == target:
            return M
 
        # Left half is sorted
        if nums[L] <= nums[M]:
            if nums[L] <= target < nums[M]:
                R = M - 1
            else:
                L = M + 1
        # Right half is sorted
        else:
            if nums[M] < target <= nums[R]:
                L = M + 1
            else:
                R = M - 1
 
    return -1
 
print(search([4,5,6,7,0,1,2], 0))  # 4
print(search([4,5,6,7,0,1,2], 3))  # -1'''
            },
            {
                "id": "LC 875",
                "title": "Koko Eating Bananas",
                "difficulty": "Medium",
                "complexity": "O(n log m) time, O(1) space",
                "description": "Find the minimum eating speed k such that Koko can eat all piles in h hours.",
                "approach": "Binary search on the answer (speed). For each speed, check if it's feasible to finish in h hours.",
                "code": '''import math
 
def minEatingSpeed(piles, h):
    L, R = 1, max(piles)
 
    while L < R:
        M = (L + R) // 2
        hours = sum(math.ceil(p / M) for p in piles)
        if hours <= h:
            R = M       # might be able to go slower
        else:
            L = M + 1   # too slow, need more speed
 
    return L
 
print(minEatingSpeed([3,6,7,11], 8))  # 4
print(minEatingSpeed([30,11,23,4,20], 5))  # 30'''
            },
            {
                "id": "LC 4",
                "title": "Median of Two Sorted Arrays",
                "difficulty": "Hard",
                "complexity": "O(log(min(m,n))) time, O(1) space",
                "description": "Find the median of two sorted arrays in O(log(m+n)) time.",
                "approach": "Binary search on partition of shorter array. Ensure left halves contain equal elements, check boundary conditions.",
                "code": '''def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1  # ensure nums1 is shorter
 
    m, n = len(nums1), len(nums2)
    L, R = 0, m
 
    while L <= R:
        i = (L + R) // 2           # partition in nums1
        j = (m + n + 1) // 2 - i   # partition in nums2
 
        maxL1 = nums1[i-1] if i > 0 else float('-inf')
        minR1 = nums1[i]   if i < m else float('inf')
        maxL2 = nums2[j-1] if j > 0 else float('-inf')
        minR2 = nums2[j]   if j < n else float('inf')
 
        if maxL1 <= minR2 and maxL2 <= minR1:
            if (m + n) % 2 == 1:
                return max(maxL1, maxL2)
            return (max(maxL1, maxL2) + min(minR1, minR2)) / 2
        elif maxL1 > minR2:
            R = i - 1
        else:
            L = i + 1
 
print(findMedianSortedArrays([1,3], [2]))    # 2.0
print(findMedianSortedArrays([1,2], [3,4]))  # 2.5'''
            },
        ]
    },

    "🪟 Sliding Window": {
        "tag": "Technique",
        "complexity": {"Fixed window": "O(n), O(1) space", "Variable window": "O(n), O(n) space"},
        "summary": (
            "Maintain a 'window' of elements that **slides** across the input. "
            "Avoids O(n²) nested loops — processes subarrays in **O(n)**."
        ),
        "content": """
### Fixed-Length Window
Window size `k` is **constant**. Slide one step at a time:
- Add incoming element (right side)
- Remove outgoing element (left side)
- Track running metric
 
### Variable-Length Window
Window size **adjusts** based on a condition:
- **Expand** right pointer while condition is valid
- **Shrink** left pointer when condition breaks
- Track best window seen so far
 
### Pattern Template
```
L = 0
for R in range(n):
    # add arr[R] to window
    while window is invalid:
        # remove arr[L] from window
        L += 1
    # update answer
```
""",
        "python_code": '''# Fixed window: max sum of k consecutive elements
def max_sum_k(arr, k):
    window_sum = sum(arr[:k])
    best = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        best = max(best, window_sum)
    return best
 
# Variable window: longest unique substring
def longest_unique(s):
    seen = set()
    L = 0; best = 0
    for R in range(len(s)):
        while s[R] in seen:
            seen.remove(s[L]); L += 1
        seen.add(s[R])
        best = max(best, R - L + 1)
    return best''',
        "leetcode_examples": [
            {
                "id": "LC 3",
                "title": "Longest Substring Without Repeating Characters",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Find the length of the longest substring without repeating characters.",
                "approach": "Sliding window with a hashset. Expand right; when duplicate found, shrink from left until valid.",
                "code": '''def lengthOfLongestSubstring(s):
    seen = set()
    L = 0
    best = 0
 
    for R in range(len(s)):
        while s[R] in seen:
            seen.remove(s[L])
            L += 1
        seen.add(s[R])
        best = max(best, R - L + 1)
 
    return best
 
print(lengthOfLongestSubstring("abcabcbb"))  # 3
print(lengthOfLongestSubstring("bbbbb"))     # 1
print(lengthOfLongestSubstring("pwwkew"))    # 3'''
            },
            {
                "id": "LC 424",
                "title": "Longest Repeating Character Replacement",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Replace at most k characters. Find longest substring with one repeated letter.",
                "approach": "Window is valid if (window_size - max_freq) <= k. Grow right, shrink left when invalid.",
                "code": '''def characterReplacement(s, k):
    count = {}
    L = 0
    max_freq = 0
    best = 0
 
    for R in range(len(s)):
        count[s[R]] = count.get(s[R], 0) + 1
        max_freq = max(max_freq, count[s[R]])
 
        # window_size - max_freq = chars to replace
        while (R - L + 1) - max_freq > k:
            count[s[L]] -= 1
            L += 1
 
        best = max(best, R - L + 1)
 
    return best
 
print(characterReplacement("ABAB", 2))   # 4
print(characterReplacement("AABABBA", 1)) # 4'''
            },
            {
                "id": "LC 567",
                "title": "Permutation in String",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Check if s2 contains a permutation of s1 as a substring.",
                "approach": "Fixed window of size len(s1). Compare character frequency arrays as window slides.",
                "code": '''def checkInclusion(s1, s2):
    if len(s1) > len(s2):
        return False
 
    count1 = [0] * 26
    count2 = [0] * 26
 
    for c in s1:
        count1[ord(c) - ord('a')] += 1
 
    for i in range(len(s2)):
        count2[ord(s2[i]) - ord('a')] += 1
        if i >= len(s1):  # slide window
            count2[ord(s2[i - len(s1)]) - ord('a')] -= 1
        if count1 == count2:
            return True
 
    return False
 
print(checkInclusion("ab", "eidbaooo"))  # True
print(checkInclusion("ab", "eidboaoo"))  # False'''
            },
            {
                "id": "LC 76",
                "title": "Minimum Window Substring",
                "difficulty": "Hard",
                "complexity": "O(n) time, O(k) space",
                "description": "Find the minimum window in s that contains all characters of t.",
                "approach": "Expand right to include chars, shrink left while window still valid. Track 'have' vs 'need' counts.",
                "code": '''from collections import Counter
 
def minWindow(s, t):
    if not t: return ""
    need = Counter(t)
    have, total_need = 0, len(need)
    L = 0
    best = (float('inf'), 0, 0)
    window = {}
 
    for R, c in enumerate(s):
        window[c] = window.get(c, 0) + 1
        if c in need and window[c] == need[c]:
            have += 1
 
        while have == total_need:
            if (R - L + 1) < best[0]:
                best = (R - L + 1, L, R)
            window[s[L]] -= 1
            if s[L] in need and window[s[L]] < need[s[L]]:
                have -= 1
            L += 1
 
    _, L, R = best
    return s[L:R+1] if best[0] != float('inf') else ""
 
print(minWindow("ADOBECODEBANC", "ABC"))  # "BANC"
print(minWindow("a", "a"))               # "a"'''
            },
            {
                "id": "LC 239",
                "title": "Sliding Window Maximum",
                "difficulty": "Hard",
                "complexity": "O(n) time, O(k) space",
                "description": "Find the maximum in each sliding window of size k.",
                "approach": "Monotonic deque storing indices in decreasing order. Front is always the current window max.",
                "code": '''from collections import deque
 
def maxSlidingWindow(nums, k):
    q = deque()   # indices, decreasing order of values
    result = []
 
    for i in range(len(nums)):
        # Remove indices outside window
        while q and q[0] < i - k + 1:
            q.popleft()
 
        # Remove smaller elements from back (they're useless)
        while q and nums[q[-1]] < nums[i]:
            q.pop()
 
        q.append(i)
 
        if i >= k - 1:
            result.append(nums[q[0]])
 
    return result
 
print(maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3))
# [3,3,5,5,6,7]'''
            },
            {
                "id": "LC 643",
                "title": "Maximum Average Subarray I",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Find the contiguous subarray of length k with the maximum average.",
                "approach": "Fixed sliding window: initialize first k elements sum, slide by adding new and removing old.",
                "code": '''def findMaxAverage(nums, k):
    window_sum = sum(nums[:k])
    best = window_sum
 
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        best = max(best, window_sum)
 
    return best / k
 
print(findMaxAverage([1,12,-5,-6,50,3], 4))  # 12.75
print(findMaxAverage([5], 1))                 # 5.0'''
            },
        ]
    },

    "🌳 Binary Trees": {
        "tag": "Trees",
        "complexity": {"BST Search (balanced)": "O(log n)", "Traversal": "O(n)", "Space": "O(n)"},
        "summary": (
            "Hierarchical structure where each node has at most **2 children**. "
            "**BSTs** enforce left < node < right for O(log n) search. "
            "Traverse with DFS (pre/in/post-order) or BFS (level-order)."
        ),
        "content": """
### Key Terms
- **Root** — topmost node
- **Leaf** — node with no children
- **Height** — longest path root → leaf
- **BST** — Binary Search Tree: left < node < right
 
### DFS Traversals
| Order | Visit pattern | Use |
|-------|--------------|-----|
| **Pre-order** | node → left → right | Copy tree |
| **In-order** | left → node → right | Sorted output (BST) |
| **Post-order** | left → right → node | Calc height |
 
### BFS (Level-order)
Uses a **queue**. Visits nodes level by level.
""",
        "python_code": '''from collections import deque
 
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
 
def in_order(node):
    if not node: return
    in_order(node.left)
    print(node.val, end=" ")
    in_order(node.right)
 
def level_order(root):
    q = deque([root])
    while q:
        node = q.popleft()
        print(node.val, end=" ")
        if node.left: q.append(node.left)
        if node.right: q.append(node.right)''',
        "leetcode_examples": [
            {
                "id": "LC 104",
                "title": "Maximum Depth of Binary Tree",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(h) space",
                "description": "Find the maximum depth (number of nodes along the longest root-to-leaf path).",
                "approach": "DFS: depth = 1 + max(depth of left, depth of right). Base case: null node returns 0.",
                "code": '''def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
 
# Iterative BFS approach
from collections import deque
def maxDepth2(root):
    if not root: return 0
    q = deque([root])
    depth = 0
    while q:
        depth += 1
        for _ in range(len(q)):
            node = q.popleft()
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
    return depth'''
            },
            {
                "id": "LC 226",
                "title": "Invert Binary Tree",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(h) space",
                "description": "Invert (mirror) a binary tree.",
                "approach": "Recursively swap left and right children of every node.",
                "code": '''def invertTree(root):
    if not root:
        return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
 
# Iterative BFS
from collections import deque
def invertTree2(root):
    if not root: return root
    q = deque([root])
    while q:
        node = q.popleft()
        node.left, node.right = node.right, node.left
        if node.left: q.append(node.left)
        if node.right: q.append(node.right)
    return root'''
            },
            {
                "id": "LC 100",
                "title": "Same Tree",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(h) space",
                "description": "Check if two binary trees are structurally identical with same node values.",
                "approach": "Recursively check: both null (same), one null (different), values differ (different), else check subtrees.",
                "code": '''def isSameTree(p, q):
    if not p and not q: return True
    if not p or not q: return False
    if p.val != q.val: return False
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)'''
            },
            {
                "id": "LC 102",
                "title": "Binary Tree Level Order Traversal",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "Return the level-order traversal as a list of lists.",
                "approach": "BFS with queue. At each level, process all nodes currently in queue (snapshot the length first).",
                "code": '''from collections import deque
 
def levelOrder(root):
    if not root: return []
    result = []
    q = deque([root])
 
    while q:
        level = []
        for _ in range(len(q)):  # process one level at a time
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        result.append(level)
 
    return result'''
            },
            {
                "id": "LC 235",
                "title": "Lowest Common Ancestor of BST",
                "difficulty": "Medium",
                "complexity": "O(log n) balanced, O(n) worst",
                "description": "Find the lowest common ancestor of two nodes in a BST.",
                "approach": "Exploit BST property: if both values < current, go left. If both > current, go right. Else current is LCA.",
                "code": '''def lowestCommonAncestor(root, p, q):
    curr = root
 
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left   # both in left subtree
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right  # both in right subtree
        else:
            return curr  # split point = LCA
 
    return None'''
            },
            {
                "id": "LC 124",
                "title": "Binary Tree Maximum Path Sum",
                "difficulty": "Hard",
                "complexity": "O(n) time, O(h) space",
                "description": "Find the maximum path sum where a path can start and end at any node.",
                "approach": "Post-order DFS. At each node, compute max gain going through left/right children. Track global max.",
                "code": '''def maxPathSum(root):
    max_sum = [float('-inf')]
 
    def dfs(node):
        if not node: return 0
        left = max(dfs(node.left), 0)   # ignore if negative
        right = max(dfs(node.right), 0)
 
        # Path through this node (can't split further up)
        max_sum[0] = max(max_sum[0], node.val + left + right)
 
        # Return max gain going in one direction (for parent)
        return node.val + max(left, right)
 
    dfs(root)
    return max_sum[0]'''
            },
            {
                "id": "LC 543",
                "title": "Diameter of Binary Tree",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(h) space",
                "description": "Find the length of the longest path between any two nodes in the tree.",
                "approach": "At each node, diameter through it = left_height + right_height. Track max during DFS.",
                "code": '''def diameterOfBinaryTree(root):
    diameter = [0]
 
    def height(node):
        if not node: return 0
        L = height(node.left)
        R = height(node.right)
        diameter[0] = max(diameter[0], L + R)
        return 1 + max(L, R)
 
    height(root)
    return diameter[0]'''
            },
        ]
    },

    "⛰️ Heaps": {
        "tag": "Trees",
        "complexity": {"Insert": "O(log n)", "Extract min/max": "O(log n)", "Peek": "O(1)", "Heapify": "O(n)"},
        "summary": (
            "A **complete binary tree** with heap property: **min-heap** has smallest at root, "
            "**max-heap** has largest. Perfect for priority queues. Python's `heapq` is a min-heap."
        ),
        "content": """
### Heap Property
- **Min-heap**: parent ≤ children → root is minimum
- **Max-heap**: parent ≥ children → root is maximum
 
### Key Operations
| Operation | Complexity |
|-----------|-----------|
| `heappush` | O(log n) |
| `heappop` | O(log n) |
| `heapify` | O(n) |
| `heap[0]` | O(1) |
 
### Python `heapq` Tip
For max-heap, **negate values**: push `-x`, pop and negate result.
""",
        "python_code": '''import heapq
 
heap = []
for num in [-4, 3, 1, 0, 2, 5]:
    heapq.heappush(heap, num)
 
print(heap[0])                   # peek → -4
smallest = heapq.heappop(heap)   # → -4
 
# Max-Heap: negate values
max_heap = []
heapq.heappush(max_heap, -9)
largest = -heapq.heappop(max_heap)  # 9''',
        "leetcode_examples": [
            {
                "id": "LC 703",
                "title": "Kth Largest Element in a Stream",
                "difficulty": "Easy",
                "complexity": "O(n log k) init, O(log k) per add",
                "description": "Design a class to find the kth largest element in a stream.",
                "approach": "Maintain a min-heap of size k. The kth largest is always at the top (minimum of the heap).",
                "code": '''import heapq
 
class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)  # keep only k largest
 
    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]  # kth largest = min of heap
 
kth = KthLargest(3, [4,5,8,2])
print(kth.add(3))   # 4
print(kth.add(5))   # 5
print(kth.add(10))  # 5'''
            },
            {
                "id": "LC 215",
                "title": "Kth Largest Element in an Array",
                "difficulty": "Medium",
                "complexity": "O(n log k) time, O(k) space",
                "description": "Find the kth largest element in an unsorted array.",
                "approach": "Min-heap of size k: push each element, pop if heap exceeds k. Final top = kth largest.",
                "code": '''import heapq
 
def findKthLargest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)  # remove smallest
    return heap[0]  # kth largest
 
# Alternative: nlargest (simpler but same complexity)
def findKthLargest2(nums, k):
    return heapq.nlargest(k, nums)[-1]
 
print(findKthLargest([3,2,1,5,6,4], 2))  # 5
print(findKthLargest([3,2,3,1,2,4,5,5,6], 4))  # 4'''
            },
            {
                "id": "LC 23",
                "title": "Merge K Sorted Lists",
                "difficulty": "Hard",
                "complexity": "O(n log k) time, O(k) space",
                "description": "Merge k sorted linked lists into one sorted list.",
                "approach": "Use min-heap of (value, index, node). Always extract minimum, add its next to heap.",
                "code": '''import heapq
 
def mergeKLists(lists):
    heap = []
    # Initialize with head of each list
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
 
    dummy = ListNode(0)
    curr = dummy
 
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
 
    return dummy.next'''
            },
            {
                "id": "LC 295",
                "title": "Find Median from Data Stream",
                "difficulty": "Hard",
                "complexity": "O(log n) add, O(1) find",
                "description": "Design a data structure that supports adding numbers and finding the median.",
                "approach": "Two heaps: max-heap for lower half, min-heap for upper half. Keep sizes balanced.",
                "code": '''import heapq
 
class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (store negated)
        self.hi = []  # min-heap
 
    def addNum(self, num):
        heapq.heappush(self.lo, -num)  # add to max-heap
 
        # Balance: lo's max must be <= hi's min
        if self.hi and (-self.lo[0]) > self.hi[0]:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
 
        # Balance sizes: lo can only be 1 bigger than hi
        if len(self.lo) > len(self.hi) + 1:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        elif len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))
 
    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0
 
mf = MedianFinder()
mf.addNum(1); mf.addNum(2)
print(mf.findMedian())  # 1.5
mf.addNum(3)
print(mf.findMedian())  # 2.0'''
            },
            {
                "id": "LC 1046",
                "title": "Last Stone Weight",
                "difficulty": "Easy",
                "complexity": "O(n log n) time, O(n) space",
                "description": "Smash the two heaviest stones. Return the remaining stone weight (0 if none left).",
                "approach": "Max-heap: always extract two heaviest, push difference back if not equal.",
                "code": '''import heapq
 
def lastStoneWeight(stones):
    heap = [-s for s in stones]  # max-heap via negation
    heapq.heapify(heap)
 
    while len(heap) > 1:
        y = -heapq.heappop(heap)  # heaviest
        x = -heapq.heappop(heap)  # second heaviest
        if x != y:
            heapq.heappush(heap, -(y - x))
 
    return -heap[0] if heap else 0
 
print(lastStoneWeight([2,7,4,1,8,1]))  # 1
print(lastStoneWeight([1]))             # 1'''
            },
            {
                "id": "LC 621",
                "title": "Task Scheduler",
                "difficulty": "Medium",
                "complexity": "O(n log n) time, O(1) space",
                "description": "Find the minimum intervals CPU needs to complete all tasks with cooldown n.",
                "approach": "Use max-heap for most frequent task. Use queue to track cooldown. Simulate time steps.",
                "code": '''import heapq
from collections import Counter, deque
 
def leastInterval(tasks, n):
    count = Counter(tasks)
    max_heap = [-c for c in count.values()]
    heapq.heapify(max_heap)
 
    time = 0
    q = deque()  # (count, time_available)
 
    while max_heap or q:
        time += 1
        if max_heap:
            cnt = 1 + heapq.heappop(max_heap)  # -1 from count
            if cnt:
                q.append((cnt, time + n))       # add cooldown
 
        if q and q[0][1] == time:
            heapq.heappush(max_heap, q.popleft()[0])
 
    return time
 
print(leastInterval(["A","A","A","B","B","B"], 2))  # 8
print(leastInterval(["A","A","A","B","B","B"], 0))  # 6'''
            },
        ]
    },

    "🔄 Recursive Backtracking": {
        "tag": "Technique",
        "complexity": {"Time": "O(2ⁿ) typical", "Space": "O(n) call stack"},
        "summary": (
            "Build solutions **incrementally**, abandoning ('backtracking') paths that violate constraints. "
            "Explores all possibilities via DFS — essential for subsets, permutations, puzzles."
        ),
        "content": """
### How It Works
Think of a **decision tree**:
- At each step: **pick** or **don't pick**
- Recurse deeper with current decision
- **Undo** (backtrack) when you return — try the other branch
 
### Template Structure
```
def backtrack(index, current_solution):
    if base_case:
        results.append(current_solution.copy())
        return
    # Option 1: skip
    backtrack(index + 1, current_solution)
    # Option 2: pick
    current_solution.append(nums[index])
    backtrack(index + 1, current_solution)
    current_solution.pop()  # ← UNDO (backtrack)
```
 
### Key Points
- Always **copy** before appending to results
- **Pop** after recursive call to undo the choice
- Use conditions to **prune** invalid paths early
""",
        "python_code": '''def subsets(nums):
    res = []
    sol = []
    def backtrack(i):
        if i == len(nums):
            res.append(sol.copy())
            return
        backtrack(i + 1)          # don't pick
        sol.append(nums[i])
        backtrack(i + 1)          # pick
        sol.pop()                 # undo
    backtrack(0)
    return res''',
        "leetcode_examples": [
            {
                "id": "LC 78",
                "title": "Subsets",
                "difficulty": "Medium",
                "complexity": "O(2ⁿ) time, O(n) space",
                "description": "Return all possible subsets (the power set) of a list of unique integers.",
                "approach": "At each index, decide: include or exclude the element. Recurse for both choices.",
                "code": '''def subsets(nums):
    res = []
    sol = []
 
    def backtrack(i):
        if i == len(nums):
            res.append(sol.copy())
            return
        # Don't include nums[i]
        backtrack(i + 1)
        # Include nums[i]
        sol.append(nums[i])
        backtrack(i + 1)
        sol.pop()  # backtrack
 
    backtrack(0)
    return res
 
print(subsets([1,2,3]))
# [[],[3],[2],[2,3],[1],[1,3],[1,2],[1,2,3]]'''
            },
            {
                "id": "LC 46",
                "title": "Permutations",
                "difficulty": "Medium",
                "complexity": "O(n! * n) time, O(n) space",
                "description": "Return all possible permutations of a list of distinct integers.",
                "approach": "At each step, try every unused number. Mark used, recurse, unmark on backtrack.",
                "code": '''def permute(nums):
    res = []
 
    def backtrack(path, used):
        if len(path) == len(nums):
            res.append(path.copy())
            return
        for i in range(len(nums)):
            if used[i]: continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()         # backtrack
            used[i] = False    # backtrack
 
    backtrack([], [False] * len(nums))
    return res
 
print(permute([1,2,3]))
# [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]'''
            },
            {
                "id": "LC 39",
                "title": "Combination Sum",
                "difficulty": "Medium",
                "complexity": "O(2^(t/m)) time",
                "description": "Find all combinations of candidates that sum to target. Can reuse elements.",
                "approach": "At each index: skip it (move to i+1) or take it (stay at i, reduce remaining). Stop when remaining < 0.",
                "code": '''def combinationSum(candidates, target):
    res = []
 
    def backtrack(i, cur, remaining):
        if remaining == 0:
            res.append(cur.copy())
            return
        if remaining < 0 or i >= len(candidates):
            return
        # Take candidates[i] (can reuse, stay at i)
        cur.append(candidates[i])
        backtrack(i, cur, remaining - candidates[i])
        cur.pop()
        # Skip candidates[i]
        backtrack(i + 1, cur, remaining)
 
    backtrack(0, [], target)
    return res
 
print(combinationSum([2,3,6,7], 7))
# [[2,2,3],[7]]'''
            },
            {
                "id": "LC 51",
                "title": "N-Queens",
                "difficulty": "Hard",
                "complexity": "O(n!) time, O(n²) space",
                "description": "Place n queens on an n×n chessboard so no two queens attack each other.",
                "approach": "Place one queen per row. Track attacked columns, diagonals, anti-diagonals as sets.",
                "code": '''def solveNQueens(n):
    cols = set()
    diag = set()      # row - col
    anti_diag = set() # row + col
    board = []
    res = []
 
    def backtrack(row):
        if row == n:
            res.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row-col) in diag or (row+col) in anti_diag:
                continue
            cols.add(col); diag.add(row-col); anti_diag.add(row+col)
            board.append(['.'] * n)
            board[-1][col] = 'Q'
            backtrack(row + 1)
            board.pop()
            cols.remove(col); diag.remove(row-col); anti_diag.remove(row+col)
 
    backtrack(0)
    return res
 
print(len(solveNQueens(4)))  # 2 solutions'''
            },
            {
                "id": "LC 79",
                "title": "Word Search",
                "difficulty": "Medium",
                "complexity": "O(n * m * 4^L) time",
                "description": "Given a board and a word, find if the word exists using adjacent cells (no reuse).",
                "approach": "DFS/backtracking from each cell. Mark cell as visited, try all 4 directions, unmark on return.",
                "code": '''def exist(board, word):
    m, n = len(board), len(board[0])
    visited = set()
 
    def dfs(r, c, idx):
        if idx == len(word): return True
        if r < 0 or c < 0 or r >= m or c >= n: return False
        if (r,c) in visited or board[r][c] != word[idx]: return False
 
        visited.add((r, c))
        res = (dfs(r+1,c,idx+1) or dfs(r-1,c,idx+1) or
               dfs(r,c+1,idx+1) or dfs(r,c-1,idx+1))
        visited.remove((r, c))  # backtrack
        return res
 
    for r in range(m):
        for c in range(n):
            if dfs(r, c, 0): return True
    return False
 
board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
print(exist(board, "ABCCED"))  # True'''
            },
            {
                "id": "LC 131",
                "title": "Palindrome Partitioning",
                "difficulty": "Medium",
                "complexity": "O(n * 2^n) time, O(n) space",
                "description": "Partition string so that every substring is a palindrome. Return all possible partitions.",
                "approach": "Backtrack: try every prefix. If it's a palindrome, recurse on remaining. Undo on backtrack.",
                "code": '''def partition(s):
    res = []
 
    def is_palindrome(sub):
        return sub == sub[::-1]
 
    def backtrack(start, path):
        if start == len(s):
            res.append(path.copy())
            return
        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if is_palindrome(sub):
                path.append(sub)
                backtrack(end, path)
                path.pop()   # backtrack
 
    backtrack(0, [])
    return res
 
print(partition("aab"))
# [['a','a','b'], ['aa','b']]'''
            },
            {
                "id": "LC 17",
                "title": "Letter Combinations of a Phone Number",
                "difficulty": "Medium",
                "complexity": "O(4^n) time, O(n) space",
                "description": "Return all possible letter combinations a phone number digits could represent.",
                "approach": "Map digits to letters. Backtrack through digits, try each corresponding letter.",
                "code": '''def letterCombinations(digits):
    if not digits: return []
    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    res = []
 
    def backtrack(i, path):
        if i == len(digits):
            res.append("".join(path))
            return
        for c in phone[digits[i]]:
            path.append(c)
            backtrack(i + 1, path)
            path.pop()  # backtrack
 
    backtrack(0, [])
    return res
 
print(letterCombinations("23"))
# ['ad','ae','af','bd','be','bf','cd','ce','cf']'''
            },
        ]
    },

    "🕸️ Graphs": {
        "tag": "Advanced",
        "complexity": {"DFS/BFS": "O(V + E)", "Space": "O(V + E)"},
        "summary": (
            "Collections of **nodes (vertices)** connected by **edges**. "
            "Represent networks, maps, social connections. "
            "Traverse with **DFS** (stack/recursion) or **BFS** (queue)."
        ),
        "content": """
### Graph Properties
- **Directed**: edges have direction (A → B ≠ B → A)
- **Undirected**: edges go both ways
- **Weighted**: edges have costs/distances
 
### Representations
| Method | Space | Best for |
|--------|-------|---------|
| **Adjacency list** | O(V+E) | Sparse graphs ✅ |
| **Adjacency matrix** | O(V²) | Dense graphs |
 
### DFS vs BFS
| | DFS | BFS |
|-|-----|-----|
| Structure | Stack / Recursion | Queue |
| Use | Paths, cycles | Shortest path (unweighted) |
 
### Must-Have: `seen` set
Always track visited nodes to **prevent infinite loops** in cyclic graphs!
""",
        "python_code": '''from collections import defaultdict, deque
 
graph = defaultdict(list)
edges = [(0,1),(1,2),(0,3)]
for u, v in edges:
    graph[u].append(v)
 
def bfs(start, graph):
    seen = {start}
    q = deque([start])
    while q:
        node = q.popleft()
        for nb in graph[node]:
            if nb not in seen:
                seen.add(nb)
                q.append(nb)''',
        "leetcode_examples": [
            {
                "id": "LC 200",
                "title": "Number of Islands",
                "difficulty": "Medium",
                "complexity": "O(m*n) time, O(m*n) space",
                "description": "Count the number of islands (groups of '1's connected horizontally/vertically).",
                "approach": "DFS from each unvisited '1'. Mark all connected land as visited. Count how many times we start a DFS.",
                "code": '''def numIslands(grid):
    if not grid: return 0
    m, n = len(grid), len(grid[0])
    count = 0
 
    def dfs(r, c):
        if r < 0 or c < 0 or r >= m or c >= n or grid[r][c] == '0':
            return
        grid[r][c] = '0'  # mark visited by sinking
        dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)
 
    for r in range(m):
        for c in range(n):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
 
    return count
 
grid = [["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]]
print(numIslands(grid))  # 3'''
            },
            {
                "id": "LC 133",
                "title": "Clone Graph",
                "difficulty": "Medium",
                "complexity": "O(V+E) time, O(V) space",
                "description": "Deep clone a connected undirected graph.",
                "approach": "BFS/DFS with a hashmap from original node to its clone. When visiting neighbors, clone if not seen.",
                "code": '''class Node:
    def __init__(self, val, neighbors=None):
        self.val = val
        self.neighbors = neighbors or []
 
def cloneGraph(node):
    if not node: return None
    clones = {}  # original -> clone
 
    def dfs(n):
        if n in clones: return clones[n]
        clone = Node(n.val)
        clones[n] = clone
        for nb in n.neighbors:
            clone.neighbors.append(dfs(nb))
        return clone
 
    return dfs(node)'''
            },
            {
                "id": "LC 417",
                "title": "Pacific Atlantic Water Flow",
                "difficulty": "Medium",
                "complexity": "O(m*n) time, O(m*n) space",
                "description": "Find cells from which water can flow to both Pacific and Atlantic oceans.",
                "approach": "Reverse BFS from ocean borders. Find cells reachable from Pacific AND Atlantic borders.",
                "code": '''from collections import deque
 
def pacificAtlantic(heights):
    m, n = len(heights), len(heights[0])
 
    def bfs(starts):
        q = deque(starts)
        visited = set(starts)
        while q:
            r, c = q.popleft()
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = r+dr, c+dc
                if (0 <= nr < m and 0 <= nc < n and
                    (nr,nc) not in visited and
                    heights[nr][nc] >= heights[r][c]):
                    visited.add((nr,nc))
                    q.append((nr,nc))
        return visited
 
    pacific = [(0,c) for c in range(n)] + [(r,0) for r in range(m)]
    atlantic = [(m-1,c) for c in range(n)] + [(r,n-1) for r in range(m)]
 
    p_reach = bfs(pacific)
    a_reach = bfs(atlantic)
 
    return [[r,c] for r,c in p_reach if (r,c) in a_reach]'''
            },
            {
                "id": "LC 207",
                "title": "Course Schedule",
                "difficulty": "Medium",
                "complexity": "O(V+E) time, O(V+E) space",
                "description": "Determine if you can finish all courses given prerequisites (detect cycle in DAG).",
                "approach": "Topological sort via DFS. Track visiting (gray), visited (black). Cycle if we revisit a gray node.",
                "code": '''from collections import defaultdict
 
def canFinish(numCourses, prerequisites):
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)  # b must come before a
 
    # 0=unvisited, 1=visiting, 2=done
    state = [0] * numCourses
 
    def dfs(node):
        if state[node] == 1: return False  # cycle!
        if state[node] == 2: return True
        state[node] = 1
        for nb in graph[node]:
            if not dfs(nb): return False
        state[node] = 2
        return True
 
    return all(dfs(i) for i in range(numCourses))
 
print(canFinish(2, [[1,0]]))        # True
print(canFinish(2, [[1,0],[0,1]]))  # False (cycle)'''
            },
            {
                "id": "LC 743",
                "title": "Network Delay Time",
                "difficulty": "Medium",
                "complexity": "O((V+E) log V) time",
                "description": "Find minimum time for signal to reach all nodes from source k. Return -1 if impossible.",
                "approach": "Dijkstra's algorithm: min-heap by distance. Greedily finalize shortest distances.",
                "code": '''import heapq
from collections import defaultdict
 
def networkDelayTime(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
 
    dist = {k: 0}
    heap = [(0, k)]  # (distance, node)
 
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float('inf')): continue
 
        for v, w in graph[u]:
            new_dist = d + w
            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))
 
    return max(dist.values()) if len(dist) == n else -1
 
print(networkDelayTime([[2,1,1],[2,3,1],[3,4,1]], 4, 2))  # 2'''
            },
            {
                "id": "LC 323",
                "title": "Number of Connected Components",
                "difficulty": "Medium",
                "complexity": "O(V+E) time, O(V+E) space",
                "description": "Count connected components in an undirected graph.",
                "approach": "DFS/BFS from each unvisited node. Each DFS start = new component.",
                "code": '''from collections import defaultdict
 
def countComponents(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
 
    seen = set()
    count = 0
 
    def dfs(node):
        seen.add(node)
        for nb in graph[node]:
            if nb not in seen:
                dfs(nb)
 
    for i in range(n):
        if i not in seen:
            dfs(i)
            count += 1
 
    return count
 
print(countComponents(5, [[0,1],[1,2],[3,4]]))  # 2
print(countComponents(5, [[0,1],[1,2],[2,3],[3,4]]))  # 1'''
            },
            {
                "id": "LC 994",
                "title": "Rotting Oranges",
                "difficulty": "Medium",
                "complexity": "O(m*n) time, O(m*n) space",
                "description": "Find minimum minutes until all fresh oranges rot. Rotten spreads to 4-neighbors each minute.",
                "approach": "Multi-source BFS from all initially rotten oranges simultaneously. Count layers = minutes.",
                "code": '''from collections import deque
 
def orangesRotting(grid):
    m, n = len(grid), len(grid[0])
    q = deque()
    fresh = 0
 
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 2: q.append((r,c,0))
            elif grid[r][c] == 1: fresh += 1
 
    minutes = 0
    while q:
        r, c, t = q.popleft()
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                minutes = t + 1
                q.append((nr, nc, t+1))
 
    return minutes if fresh == 0 else -1
 
print(orangesRotting([[2,1,1],[1,1,0],[0,1,1]]))  # 4
print(orangesRotting([[2,1,1],[0,1,1],[1,0,1]]))  # -1'''
            },
        ]
    },

    "💡 Dynamic Programming": {
        "tag": "Advanced",
        "complexity": {"Memoization": "O(n) time, O(n) space", "Tabulation": "O(n) time, O(n) space", "Optimized": "O(n) time, O(1) space"},
        "summary": (
            "Solve complex problems by **caching subproblem results** to avoid recomputation. "
            "Key insight: **overlapping subproblems** + **optimal substructure** → DP."
        ),
        "content": """
### When to Use DP
Signs a problem needs DP:
- Can be broken into **smaller subproblems**
- **Same subproblems** appear multiple times
- Optimizing something: min cost, max value, count ways
 
### 4-Step Progression
 
**Step 1 — Naive Recursion**: Direct recurrence. **O(2ⁿ)** — too slow.
 
**Step 2 — Memoization (Top-Down)**: Add a cache. **O(n) time, O(n) space**.
 
**Step 3 — Tabulation (Bottom-Up)**: Build from base cases. No recursion overhead.
 
**Step 4 — Space Optimization**: Drop full array → **O(1) space**.
""",
        "python_code": '''# Fibonacci — space-optimized O(1)
def fib(n):
    if n <= 1: return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
 
# Coin change: min coins to make amount
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1''',
        "leetcode_examples": [
            {
                "id": "LC 70",
                "title": "Climbing Stairs",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Count distinct ways to climb n stairs (can climb 1 or 2 steps at a time).",
                "approach": "Fibonacci pattern. dp[n] = dp[n-1] + dp[n-2]. Space-optimize to just two variables.",
                "code": '''def climbStairs(n):
    if n <= 2: return n
    prev, curr = 1, 2
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr
 
print(climbStairs(2))  # 2 (1+1, 2)
print(climbStairs(3))  # 3 (1+1+1, 1+2, 2+1)
print(climbStairs(5))  # 8'''
            },
            {
                "id": "LC 322",
                "title": "Coin Change",
                "difficulty": "Medium",
                "complexity": "O(amount * coins) time, O(amount) space",
                "description": "Find the minimum number of coins to make up a given amount. Return -1 if impossible.",
                "approach": "Bottom-up DP: dp[a] = min coins to make amount a. For each amount, try each coin.",
                "code": '''def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # base case: 0 coins for amount 0
 
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
 
    return dp[amount] if dp[amount] != float('inf') else -1
 
print(coinChange([1,5,11], 15))  # 3 (5+5+5)
print(coinChange([2], 3))         # -1'''
            },
            {
                "id": "LC 300",
                "title": "Longest Increasing Subsequence",
                "difficulty": "Medium",
                "complexity": "O(n²) DP, O(n log n) with patience sort",
                "description": "Find the length of the longest strictly increasing subsequence.",
                "approach": "dp[i] = LIS ending at index i. For each i, check all j < i where nums[j] < nums[i].",
                "code": '''def lengthOfLIS(nums):
    n = len(nums)
    dp = [1] * n  # each element alone is LIS of length 1
 
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
 
    return max(dp)
 
# O(n log n) with binary search
import bisect
def lengthOfLIS2(nums):
    sub = []  # stores the smallest tail for LIS of each length
    for num in nums:
        pos = bisect.bisect_left(sub, num)
        if pos == len(sub): sub.append(num)
        else: sub[pos] = num
    return len(sub)
 
print(lengthOfLIS([10,9,2,5,3,7,101,18]))  # 4'''
            },
            {
                "id": "LC 416",
                "title": "Partition Equal Subset Sum",
                "difficulty": "Medium",
                "complexity": "O(n * sum) time, O(sum) space",
                "description": "Determine if array can be partitioned into two subsets with equal sum.",
                "approach": "If total sum is odd → impossible. Otherwise, find if subset summing to total//2 exists.",
                "code": '''def canPartition(nums):
    total = sum(nums)
    if total % 2 != 0: return False
    target = total // 2
 
    dp = {0}  # set of achievable sums
    for num in nums:
        dp = {s + num for s in dp} | dp
        if target in dp: return True
 
    return target in dp
 
# Alternative: boolean DP array
def canPartition2(nums):
    target = sum(nums)
    if target % 2: return False
    target //= 2
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
    return dp[target]
 
print(canPartition([1,5,11,5]))  # True (1+5+5 = 11)
print(canPartition([1,2,3,5]))   # False'''
            },
            {
                "id": "LC 1143",
                "title": "Longest Common Subsequence",
                "difficulty": "Medium",
                "complexity": "O(m*n) time, O(m*n) space",
                "description": "Find the length of the longest common subsequence of two strings.",
                "approach": "2D DP table. If chars match, dp[i][j] = dp[i-1][j-1] + 1. Else take max of skipping either char.",
                "code": '''def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
 
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
 
    return dp[m][n]
 
print(longestCommonSubsequence("abcde", "ace"))  # 3
print(longestCommonSubsequence("abc", "abc"))     # 3
print(longestCommonSubsequence("abc", "def"))     # 0'''
            },
            {
                "id": "LC 72",
                "title": "Edit Distance",
                "difficulty": "Hard",
                "complexity": "O(m*n) time, O(m*n) space",
                "description": "Find the minimum number of operations (insert, delete, replace) to convert word1 to word2.",
                "approach": "2D DP. If chars match, no cost. Otherwise, min of three operations (insert, delete, replace) + 1.",
                "code": '''def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
 
    # Base cases
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
 
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # delete from word1
                    dp[i][j-1],    # insert into word1
                    dp[i-1][j-1]   # replace
                )
 
    return dp[m][n]
 
print(minDistance("horse", "ros"))    # 3
print(minDistance("intention", "execution"))  # 5'''
            },
            {
                "id": "LC 91",
                "title": "Decode Ways",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Count number of ways to decode a string of digits (A=1, B=2, ..., Z=26).",
                "approach": "DP where dp[i] = number of ways to decode s[:i]. Single digit valid if non-zero; double digit valid if 10-26.",
                "code": '''def numDecodings(s):
    if not s or s[0] == '0': return 0
 
    n = len(s)
    # dp[i] = ways to decode s[:i]
    prev2, prev1 = 1, 1  # dp[0], dp[1]
 
    for i in range(2, n + 1):
        curr = 0
        one_digit = int(s[i-1])
        two_digit = int(s[i-2:i])
 
        if one_digit >= 1:         # valid single digit
            curr += prev1
        if 10 <= two_digit <= 26:  # valid double digit
            curr += prev2
 
        prev2, prev1 = prev1, curr
 
    return prev1
 
print(numDecodings("12"))    # 2 (AB, L)
print(numDecodings("226"))   # 3 (BZ, VF, BBF)
print(numDecodings("06"))    # 0'''
            },
        ]
    },
}

# ── TOPIC SELECTION ───────────────────────────────────────────────────────────

topic_keys = list(TOPICS.keys())

selected_topic = st.selectbox(
    "📚 Select a Topic",
    topic_keys,
    index=0,
    help="Choose a DSA topic to study"
)

topic_name = selected_topic
topic = TOPICS[topic_name]

# ── MAIN CONTENT ──────────────────────────────────────────────────────────────

col_title, col_tag = st.columns([5, 1])
with col_title:
    st.title(topic_name)
with col_tag:
    st.markdown(
        f"<br><span style='background:#1e3a5f;color:#7dd3fc;padding:4px 12px;border-radius:12px;font-size:0.85em;'>{topic['tag']}</span>", unsafe_allow_html=True)

st.info(topic["summary"])

# Complexity badges
st.markdown("**⏱ Complexity**")
cols = st.columns(len(topic["complexity"]))
for i, (label, value) in enumerate(topic["complexity"].items()):
    with cols[i]:
        st.metric(label=label, value=value)

st.divider()

# Special section for Big O complexities table
if "complexities" in topic:
    st.subheader("Common Complexity Classes")
    for notation, description, rating in topic["complexities"]:
        col1, col2, col3 = st.columns([1.2, 4, 1])
        with col1:
            st.code(notation)
        with col2:
            st.write(description)
        with col3:
            st.write(rating)
    st.divider()

# Tabs: Concept + Code + LeetCode
tab1, tab2, tab3 = st.tabs(["📖 Concept", "🐍 Core Code", "🟨 LeetCode Examples"])

with tab1:
    st.markdown(topic["content"])

with tab2:
    st.code(topic["python_code"], language="python")

with tab3:
    examples = topic.get("leetcode_examples", [])
    if not examples:
        st.info("No LeetCode examples available for this topic yet.")
    else:
        st.markdown(f"### {len(examples)} LeetCode Problems")
        for ex in examples:
            diff_color = {"Easy": "🟢", "Medium": "🟡",
                          "Hard": "🔴"}.get(ex["difficulty"], "⚪")
            with st.expander(f"{diff_color} **{ex['id']} — {ex['title']}** · `{ex['difficulty']}` · {ex['complexity']}"):
                st.markdown(f"**Problem:** {ex['description']}")
                st.markdown(f"**Approach:** {ex['approach']}")
                st.code(ex["code"], language="python")

# ── FOOTER ────────────────────────────────────────────────────────────────────

st.divider()
st.caption(
    "📖 Based on [AlgoMap.io](https://algomap.io) roadmap · Problems from [LeetCode](https://leetcode.com)")
