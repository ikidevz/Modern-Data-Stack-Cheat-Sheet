import streamlit as st
from utility.seo import inject_seo
from components import sidebar

st.set_page_config(
    page_title="Data Structure & Algorithm - Modern Data Stack Cheat Sheet",
    page_icon="🧠",
    layout="wide",
)
sidebar()
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
        if arr[M] == target:
            return True
        elif arr[M] < target:
            L = M + 1
        else:
            R = M - 1
    return False


# O(n log n) - Linearithmic
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):  # linear merge
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# O(2^n) - Exponential
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)  # 2 recursive calls''',
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
                "id": "LC 2239",
                "title": "Find Closest Number to Zero",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Given an integer array nums of size n, return the number with the value closest to 0 in nums. If there are multiple answers, return the number with the largest value.",
                "approach": "This problem is typically solved using a linear scan algorithm. We initialize a variable, commonly called closest, with the first value of the array. As we iterate through the array, we compare each element using absolute value comparison: If the absolute value of the current number is less than that of closest, update closest. If the absolute values are the same, choose the positive number. This logic ensures that we return the number closest to zero and correctly handle tie-breakers in favor of positive values.",
                "code": '''from typing import List
 
def findClosestNumber(nums: List[int]) -> int:
    closest = nums[0]
    for x in nums:
        if abs(x) < abs(closest):
            closest = x
    
    if closest < 0 and abs(closest) in nums:
        return abs(closest)
    else:
        return closest'''
            },
            {
                "id": "LC 1768",
                "title": "Merge Strings Alternately",
                "difficulty": "Easy",
                "complexity": "O(T) time, O(T) space",
                "description": "You are given two strings, word1 and word2. The task is to create a new string by merging characters alternately from each input. You begin with the first character of word1, followed by the first character of word2, then the second from word1, and so on. This continues until all characters from both strings are used. If one string is longer than the other, the remaining characters from the longer string are appended at the end.",
                "approach": "First, import the zip_longest function from Python’s itertools module. You then use it to pair each character from word1 and word2. If one string is shorter, zip_longest fills in the gap with an empty string so the loop can continue without errors. For every paired set of characters, concatenate them and build the merged result as a single combined string. The final result is simply the join of all such pairs.",
                "code": '''def mergeAlternately(self, word1: str, word2: str) -> str:
    A, B = len(word1), len(word2)
    a, b = 0, 0
    s = []

    word = 1
    while a < A and b < B:
        if word == 1:
            s.append(word1[a])
            a += 1
            word = 2
        else:
            s.append(word2[b])
            b += 1
            word = 1
    
    while a < A:
        s.append(word1[a])
        a += 1
    
    while b < B:
        s.append(word2[b])
        b += 1
    
    return ''.join(s)'''
            },
            {
                "id": "LC 13",
                "title": "Roman to Integer",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "You are given a Roman numeral string. Convert it to an integer. Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.",
                "approach": "Iterate through the string from left to right. For each character, check if it forms a special case with the next character (like IV or IX). If so, subtract the value of the current character from the next one and add the result to the total. Otherwise, simply add the value of the current character to the total.",
                "code": '''def romanToInt(self, s: str) -> int:
    d = {'I': 1, 'V':5, 'X':10, 'L':50, 'C':100, 'D': 500, 'M':1000}
    summ = 0
    n = len(s)
    i = 0
    
    while i < n:
        if i < n - 1 and d[s[i]] < d[s[i+1]]:
            summ += d[s[i+1]] - d[s[i]]
            i += 2
        else:
            summ += d[s[i]]
            i += 1
    
    return summ'''
            },
            {
                "id": "LC 392",
                "title": "Is Subsequence",
                "difficulty": "Easy",
                "complexity": "O(T) time, O(1) space",
                "description": "Given two strings s and t, determine if s is a subsequence of t.",
                "approach": "Use two pointers to traverse both strings. Move the pointer for t always, and move the pointer for s only when a matching character is found. If we reach the end of s, it means s is a subsequence of t.",
                "code": '''def isSubsequence(self, s: str, t: str) -> bool:
    S = len(s)
    T = len(t)
    if s == '': return True
    if S > T: return False

    j = 0
    for i in range(T):
        if t[i] == s[j]:
            if j == S-1:
                return True
            j += 1
    
    return False'''
            },
            {
                "id": "LC 121",
                "title": "Best Time to Buy and Sell Stock",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "You are given an array prices where prices[i] is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.",
                "approach": "Initialize two variables: min_price to track the lowest price seen so far, and max_profit to track the maximum profit. Iterate through the list of prices. For each price, update min_price if the current price is lower. Calculate the potential profit by subtracting min_price from the current price. If this potential profit is greater than max_profit, update max_profit. After iterating through all prices, return max_profit.",
                "code": '''def maxProfit(prices: List[int]) -> int:
    # Time: O(n)
    # Space: O(1)
    min_price = float('inf')
    max_profit = 0        
    
    for price in prices:
        if price < min_price:
            min_price = price
        
        profit = price - min_price
    
        if profit > max_profit:
            max_profit = profit
            
    return max_profit'''
            },
            {
                "id": "LC 14",
                "title": "Longest Common Prefix",
                "difficulty": "Easy",
                "complexity": " O(n * m) time, O(1) space",
                "description": "Find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string.",
                "approach": "Find the minimum length among all strings. Iterate through each character position up to the minimum length. For each position, check if all strings have the same character. If so, add it to the result; otherwise, return the result.",
                "code": '''def longestCommonPrefix(strs: List[str]) -> str:
    min_length = float('inf')

    for s in strs:
        if len(s) < min_length:
            min_length = len(s)
    
    i = 0
    while i < min_length:
        for s in strs:
            if s[i] != strs[0][i]:
                return s[:i]
        i += 1
    
    return strs[0][:i]'''
            },
            {
                "id": "LC 228",
                "title": "Summary Ranges",
                "difficulty": "Easy",
                "complexity": " O(n) time, O(n) space",
                "description": "Given a sorted integer array without duplicates, return the smallest sorted list of ranges that cover all the numbers in the array.",
                "approach": "Iterate through the array and keep track of the start and end of each range. When a number is not consecutive to the previous one, finalize the current range and start a new one.",
                "code": '''def summaryRanges(nums: List[int]) -> List[str]:
        ans = []     
        i = 0 
        
        while i < len(nums): 
            start = nums[i]  
            while i < len(nums)-1 and nums[i] + 1 == nums[i + 1]: 
                i += 1 
            
            if start != nums[i]: 
                ans.append(str(start) + "->" + str(nums[i]))
            else: 
                ans.append(str(nums[i]))
            
            i += 1
 
        return ans'''
            },
            {
                "id": "LC 238",
                "title": "Product of Array Except Self",
                "difficulty": "Medium",
                "complexity": " O(n) time, O(n) space",
                "description": "Given an integer array, return an array where each element at index i is the product of all elements in the array except the one at index i.",
                "approach": "Iterate through the array and for each element, calculate the product of all other elements.",
                "code": '''def productExceptSelf(nums: List[int]) -> List[int]:
    l_mult = 1
    r_mult = 1
    n = len(nums)
    l_arr = [0] * n
    r_arr = [0] * n
    
    for i in range(n): 
        j = -i -1
        l_arr[i] = l_mult
        r_arr[j] = r_mult
        l_mult *= nums[i]
        r_mult *= nums[j]

    return [l*r for l, r in zip(l_arr, r_arr)]'''
            },
            {
                "id": "LC 54",
                "title": "Spiral Matrix",
                "difficulty": "Medium",
                "complexity": " O(m*n) time, O(1) space",
                "description": "Given an m x n matrix, return all elements of the matrix in spiral order.",
                "approach": "Traverse the matrix in a spiral pattern, keeping track of the boundaries.",
                "code": '''def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
    m, n = len(matrix), len(matrix[0])
    ans = []
    i, j = 0, 0
    UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
    direction = RIGHT

    UP_WALL = 0
    RIGHT_WALL = n
    DOWN_WALL = m
    LEFT_WALL = -1

    while len(ans) != m*n:
        if direction == RIGHT:
            while j < RIGHT_WALL:
                ans.append(matrix[i][j])
                j += 1
            i, j = i+1, j-1
            RIGHT_WALL -= 1
            direction = DOWN
        elif direction == DOWN:
            while i < DOWN_WALL:
                ans.append(matrix[i][j])
                i += 1
            i, j = i-1, j-1
            DOWN_WALL -= 1
            direction = LEFT
        elif direction == LEFT:
            while j > LEFT_WALL:
                ans.append(matrix[i][j])
                j -= 1
            i, j = i-1, j+1
            LEFT_WALL += 1
            direction = UP
        else:
            while i > UP_WALL:
                ans.append(matrix[i][j])
                i -= 1
            i, j = i+1, j+1
            UP_WALL += 1
            direction = RIGHT
    
    return ans'''
            },
            {
                "id": "LC 56",
                "title": "Merge Intervals",
                "difficulty": "Medium",
                "complexity": " O(n log n) time, O(n) space",
                "description": "Given an array of intervals, merge all overlapping intervals.",
                "approach": "Sort the intervals by their start times. Then iterate through the sorted intervals and merge any overlapping ones.",
                "code": '''def merge(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort(key=lambda interval: interval[0])
    merged = []

    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1] = [merged[-1][0], max(merged[-1][1], interval[1])]
    
    return merged'''
            },
            {
                "id": "LC 48",
                "title": "Rotate Image",
                "difficulty": "Medium",
                "complexity": " O(n^2) time, O(1) space",
                "description": "You are given an n x n 2D matrix representing an image. Rotate the image by 90 degrees (clockwise).",
                "approach": "First transpose the matrix, then reverse each row.",
                "code": '''def rotate(self, matrix: List[List[int]]) -> None:
    n = len(matrix)
    
    # Tranpose
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Reflection
    for i in range(n):
        for j in range(n // 2):
            matrix[i][j], matrix[i][n-j-1] = matrix[i][n-j-1], matrix[i][j]'''
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

# ============================================================
# 1. Detect duplicates (O(n))
# ============================================================

def has_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False

# Sample usage
print(has_duplicate([1, 2, 3, 4]))      # False
print(has_duplicate([1, 2, 3, 1]))      # True


# ============================================================
# 2. Two Sum (HashMap)
# ============================================================

def two_sum(nums, target):
    lookup = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in lookup:
            return [lookup[diff], i]
        lookup[num] = i
    return []

# Sample usage
print(two_sum([2, 7, 11, 15], 9))       # [0, 1]


# ============================================================
# 3. Group Anagrams
# ============================================================

def group_anagrams(strs):
    groups = defaultdict(list)
    for word in strs:
        key = tuple(sorted(word))
        groups[key].append(word)
    return list(groups.values())

# Sample usage
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]


# ============================================================
# 4. Character Count
# ============================================================

def char_count(s):
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    return freq

# Sample usage
print(char_count("banana"))   # {'b':1,'a':3,'n':2}


# ============================================================
# 5. Counter (built-in)
# ============================================================

def count_chars(s):
    return Counter(s)

# Sample usage
print(count_chars("banana"))  # Counter({'a':3,'n':2,'b':1})''',
        "leetcode_examples": [
            {
                "id": "LC 771",
                "title": "Jewels and Stones",
                "difficulty": "Easy",
                "complexity": "O(n + m) time, O(n) space",
                "description": "You're given strings jewels representing the types of stones that are jewels, and stones representing the stones you have. Each character in stones is a type of stone you have. You want to know how many of the stones you have are also jewels.",
                "approach": "To solve this problem, we can use a set to store the types of jewels for O(1) average time complexity lookups. We then iterate through the stones and count how many of them are in the set of jewels.",
                "code": ''' def numJewelsInStones (jewels: str, stones: str) -> int:
    # O(n + m)
    s = set(jewels)
    count = 0
    for stone in stones:
        if stone in s:
            count += 1
    return count'''
            },
            {
                "id": "LC 217",
                "title": "Contains Duplicate",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Return true if any value appears at least twice in the array.",
                "approach": "Add each element to a set. If element already in set → duplicate found.",
                "code": ''' def containsDuplicate(nums: list[int]) -> bool:
    s = set()
    for num in nums:
        if num in s:
            return True
        else:
            s.add(num)
    return False'''
            },

            {
                "id": "LC 383",
                "title": "Ransom Note",
                "difficulty": "Easy",
                "complexity": "O(R + M) time, O(M) space",
                "description": "Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine and false otherwise. Each letter in magazine can only be used once in ransomNote.",
                "approach": "Use a hash map to count the frequency of each character in magazine. Then, iterate through ransomNote and check if the required characters are available in the hash map with sufficient frequency. If any character is missing or insufficient, return false. If we successfully check all characters, return true.",
                "code": '''def canConstruct(ransomNote: str, magazine: str) -> bool:
    hashmap = Counter(magazine) # TC for Counter is O(n)

    for ch in ransomNote:
        if hashmap[ch] > 0:
            hashmap[ch]-=1
        else:
            return False
    return True'''
            },
            {
                "id": "LC 242",
                "title": "Valid Anagram",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Given two strings s and t, return true if t is an anagram of s, and false otherwise. An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
                "approach": "To determine if two strings are anagrams, we can count the frequency of each character in both strings and compare the counts. If the counts are the same for all characters, then the strings are anagrams of each other.",
                "code": '''def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    s_dict = Counter(s)
    t_dict = Counter(t)

    return s_dict == t_dict'''
            },
            {
                "id": "LC 1189",
                "title": "Maximum Number of Balloons",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Given a string text, return the maximum number of times we can form the word \"balloon\" using the characters from text.",
                "approach": "Count the frequency of each character in the input string. Then, determine how many complete instances of \"balloon\" can be formed based on the available characters.",
                "code": '''def maxNumberOfBalloons(text: str) -> int:
    counter = defaultdict(int)
    balloon = "balloon"
    
    for c in text:
        if c in balloon:
            counter[c] += 1
    
    if any(c not in counter for c in balloon):
        return 0
    else:
        return min(counter["b"], counter["a"], counter["l"] // 2, counter["o"] // 2, counter["n"])'''
            },
            {
                "id": "LC 1",
                "title": "Two Sum",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                "approach": "Use a hash map to store the indices of elements as we iterate through the array. For each element, calculate its complement and check if the complement is already in the hash map.",
                "code": '''def twoSum(nums: List[int], target: int) -> List[int]:
    h = {}
    for i in range(len(nums)):
        h[nums[i]] = i

    for i in range(len(nums)):
        y = target - nums[i]

        if y in h and h[y] != i:
            return [i, h[y]]'''
            },
            {
                "id": "LC 169",
                "title": "Majority Element",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Given an array nums of size n, return the majority element. The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.",
                "approach": "Use Boyer-Moore Majority Vote Algorithm to find the majority element in linear time and constant space.",
                "code": '''def majorityElement(nums: List[int]) -> int:
    candidate = None
    count = 0

    for num in nums:
        if count == 0:
            candidate = num
        
        count += 1 if candidate == num else -1
    
    return candidate'''
            },
            {
                "id": "LC 36",
                "title": "Valid Sudoku",
                "difficulty": "Medium",
                "complexity": "O(n^2) time, O(n) space",
                "description": "Determine if a 9x9 Sudoku board is valid according to the rules.",
                "approach": "Check each row, column, and 3x3 box for duplicate values.",
                "code": '''def isValidSudoku(self, board: List[List[str]]) -> bool:
    # Validate Rows
    for i in range(9):
        s = set()
        for j in range(9):
            item = board[i][j]
            if item in s:
                return False
            elif item != '.':
                s.add(item)
    
    # Validate Cols
    for i in range(9):
        s = set()
        for j in range(9):
            item = board[j][i]
            if item in s:
                return False
            elif item != '.':
                s.add(item)
        
    # Validate Boxes
    starts = [(0, 0), (0, 3), (0, 6),
                (3, 0), (3, 3), (3, 6),
                (6, 0), (6, 3), (6, 6)]
    
    for i, j in starts:
        s = set()
        for row in range(i, i+3):
            for col in range(j, j+3):
                item = board[row][col]
                if item in s:
                    return False
                elif item != '.':
                    s.add(item)
    return True'''
            },
            {
                "id": "LC 49",
                "title": "Group Anagrams",
                "difficulty": "Medium",
                "complexity": "O(n * m) time,  O(n * m) space",
                "description": "Given an array of strings, group anagrams together.",
                "approach": "Use a hash map to store lists of anagrams. For each string, sort its characters and use the sorted string as a key.",
                "code": '''from collections import defaultdict

def groupAnagrams(strs: List[str]) -> List[List[str]]:
    anagrams_dict = defaultdict(list)
    for s in strs: # n
        count = [0] * 26
        for c in s:
            count[ord(c) - ord("a")] += 1
        key = tuple(count)
        anagrams_dict[key].append(s)

    return anagrams_dict.values()'''
            },
            {
                "id": "LC 128",
                "title": "Longest Consecutive Sequence",
                "difficulty": "Hard",
                "complexity": "O(n) time,  O(n) space",
                "description": "Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence. The consecutive elements sequence is a sequence of integers where each integer is one more than the previous integer. The longest consecutive elements sequence is the longest such sequence that can be found in nums.",
                "approach": "Use a set to store the unique numbers. For each number, check if it's the start of a sequence (i.e., num - 1 is not in the set). If it is, count how long the sequence is by checking for num + 1, num + 2, etc. Keep track of the longest sequence found.",
                "code": '''def longestConsecutive(nums: List[int]) -> int:
    s = set(nums)
    longest = 0

    for num in s:
        if num - 1 not in s:
            next_num = num + 1
            length = 1
            while next_num in s:
                length += 1
                next_num += 1
            longest = max(longest, length)
    
    return longest'''
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
        "python_code": '''
# ============================================================
# 1. Two Sum (Sorted)
# ============================================================

def two_sum_sorted(arr, target):
    L, R = 0, len(arr) - 1
    while L < R:
        total = arr[L] + arr[R]
        if total == target:
            return [L, R]
        elif total < target:
            L += 1
        else:
            R -= 1
    return []

# Sample usage
print(two_sum_sorted([1, 2, 3, 4, 6], 6))   # [1, 3]


# ============================================================
# 2. Palindrome Check
# ============================================================

def is_palindrome(s):
    L, R = 0, len(s) - 1
    while L < R:
        if s[L] != s[R]:
            return False
        L += 1
        R -= 1
    return True

# Sample usage
print(is_palindrome("racecar"))   # True
print(is_palindrome("hello"))     # False


# ============================================================
# 3. Remove Duplicates (Sorted Array)
# ============================================================

def remove_duplicates(arr):
    if not arr:
        return 0

    write = 1
    for read in range(1, len(arr)):
        if arr[read] != arr[read - 1]:
            arr[write] = arr[read]
            write += 1

    return write

# Sample usage
arr = [1, 1, 2, 2, 3]
k = remove_duplicates(arr)
print(arr[:k])   # [1, 2, 3]


# ============================================================
# 4. Move Zeroes
# ============================================================

def move_zeroes(nums):
    insert = 0
    for num in nums:
        if num != 0:
            nums[insert] = num
            insert += 1

    for i in range(insert, len(nums)):
        nums[i] = 0

# Sample usage
nums = [0, 1, 0, 3, 12]
move_zeroes(nums)
print(nums)   # [1, 3, 12, 0, 0]


# ============================================================
# 5. Reverse String
# ============================================================

def reverse_string(s):
    s = list(s)
    L, R = 0, len(s) - 1
    while L < R:
        s[L], s[R] = s[R], s[L]
        L += 1
        R -= 1
    return "".join(s)

# Sample usage
print(reverse_string("hello"))   # "olleh"


# ============================================================
# 6. Container With Most Water
# ============================================================

def max_area(height):
    L, R = 0, len(height) - 1
    max_water = 0

    while L < R:
        h = min(height[L], height[R])
        width = R - L
        max_water = max(max_water, h * width)

        if height[L] < height[R]:
            L += 1
        else:
            R -= 1

    return max_water

# Sample usage
print(max_area([1,8,6,2,5,4,8,3,7]))   # 49


# ============================================================
# 7. Valid Palindrome (Ignore Symbols)
# ============================================================

def is_valid_palindrome(s):
    L, R = 0, len(s) - 1

    while L < R:
        while L < R and not s[L].isalnum():
            L += 1
        while L < R and not s[R].isalnum():
            R -= 1

        if s[L].lower() != s[R].lower():
            return False

        L += 1
        R -= 1

    return True

# Sample usage
print(is_valid_palindrome("A man, a plan, a canal: Panama"))  # True''',
        "leetcode_examples": [
            {
                "id": "LC 977",
                "title": "Squares of a Sorted Array",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "You are given an integer array nums sorted in non-decreasing order. Return an array of the squares of each number sorted in non-decreasing order.",
                "approach": "Two pointers approach: We can use two pointers, one starting at the beginning of the array and the other at the end. We compare the absolute values of the elements at these pointers, square the larger one, and add it to the result array. We then move the pointer that had the larger absolute value. Finally, we reverse the result array to get the correct order.",
                "code": '''def sortedSquares(nums: List[int]) -> List[int]:
    left = 0
    right = len(nums) - 1
    result = []

    while left <= right:
        if abs(nums[left]) > abs(nums[right]):
            result.append(nums[left] ** 2)
            left += 1
        else:
            result.append(nums[right] ** 2)
            right -= 1

    result.reverse()

    return result'''
            },
            {
                "id": "LC 344",
                "title": "Reverse String",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Write a function that reverses a string. The input string is given as an array of characters s.",
                "approach": "Use two pointers, one starting at the beginning and the other at the end. Swap the characters at these pointers and move them towards each other until they meet.",
                "code": '''def reverseString(self, s: List[str]) -> None:
    n = len(s)
    l = 0
    r = n - 1

    while l < r:
        s[l], s[r] = s[r], s[l]
        l += 1
        r -= 1'''
            },
            {
                "id": "LC 125",
                "title": "Valid Palindrome",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Given a string s, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.",
                "approach": "Use two pointers, one starting at the beginning and the other at the end. Skip non-alphanumeric characters and compare the remaining characters.",
                "code": '''def isPalindrome(self, s: str) -> bool:
    n = len(s)
    L = 0
    R = n - 1

    while L < R:
        if not s[L].isalnum():
            L += 1
            continue

        if not s[R].isalnum():
            R -= 1
            continue

        if s[L].lower() != s[R].lower():
            return False

        L += 1
        R -= 1

    return True'''
            },
            {
                "id": "LC 167",
                "title": "Two Sum II",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length. Return the indices of the two numbers, index1 and index2, added by one as an integer array [index1, index2] of length 2.",
                "approach": "Use two pointers, one starting at the beginning and the other at the end. Calculate the sum of the elements at these pointers. If the sum is equal to the target, return the indices. If the sum is less than the target, move the left pointer to the right. If the sum is greater than the target, move the right pointer to the left.",
                "code": '''def twoSum(self, numbers: List[int], target: int) -> List[int]:
    n = len(numbers)
    l = 0
    r = n - 1

    while l < r:
        summ = numbers[l] + numbers[r]
        if summ == target:
            return [l + 1, r + 1]
        elif summ < target:
            l += 1
        else:
            r -= 1'''
            },
            {
                "id": "LC 15",
                "title": "Three Sum",
                "difficulty": "Medium",
                "complexity": "O(n^2) time, O(n) space",
                "description": "Given an array nums of n integers, return an array of all the unique triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.",
                "approach": "Sort the array first. Then, for each element, use two pointers to find pairs that sum to the negative of the current element.",
                "code": '''def threeSum(nums: List[int]) -> List[List[int]]:
    nums.sort()
    n = len(nums)
    answer = []
    for i in range(n):
        if nums[i] > 0:
            break
        elif i > 0 and nums[i] == nums[i-1]:
            continue
        lo, hi = i+1, n-1
        while lo < hi:
            summ = nums[i] + nums[lo] + nums[hi]
            if summ == 0:
                answer.append([nums[i], nums[lo], nums[hi]])
                lo, hi = lo+1, hi-1
                while lo < hi and nums[lo] == nums[lo-1]:
                    lo += 1
                while lo < hi and nums[hi] == nums[hi+1]:
                    hi -= 1
            elif summ < 0:
                lo += 1
            else:
                hi -= 1
    
    return answer'''
            },
            {
                "id": "LC 11",
                "title": "Container With Most Water",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]). Find two lines that together with the x-axis form a container, such that the container contains the most water.",
                "approach": "Use two pointers, one starting at the beginning and the other at the end. Calculate the area formed by these pointers and move the pointer pointing to the shorter line towards the other pointer.",
                "code": '''def maxArea(self, height: List[int]) -> int:
    n = len(height)
    l = 0
    r = n - 1
    max_area = 0

    while l < r:
        w = r - l
        h = min(height[l], height[r])
        a = w * h
        max_area = max(max_area, a)
        
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1

    return max_area'''
            },

            {
                "id": "LC 42",
                "title": "Trapping Rain Water",
                "difficulty": "Hard",
                "complexity": "O(n) time, O(n) space",
                "description": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
                "approach": "First, we can precompute the maximum height to the left and right of each bar. Then, for each bar, the amount of water it can trap is the minimum of the maximum heights on its left and right minus its own height. We sum this up for all bars to get the total trapped water.",
                "code": '''def trap(height: List[int]) -> int:
    l_wall = r_wall = 0
    n = len(height)
    max_left = [0] * n
    max_right = [0] * n

    for i in range(n):
        j = -i - 1
        max_left[i] = l_wall
        max_right[j] = r_wall
        l_wall = max(l_wall, height[i])
        r_wall = max(r_wall, height[j])

    summ = 0
    for i in range(n):
        pot = min(max_left[i], max_right[i])
        summ += max(0, pot - height[i])

    return summ'''
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

# ============================================================
# STACK (LIFO - Last In, First Out)
# ============================================================

stack = []

# Push (O(1))
stack.append(5)
stack.append(4)
stack.append(3)

# Peek (O(1))
print(stack[-1])   # 3

# Pop (O(1))
print(stack.pop()) # 3
print(stack)       # [5, 4]


# ============================================================
# 1. VALID PARENTHESES (STACK) 🔥
# ============================================================

def is_valid_parentheses(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for c in s:
        if c in mapping:
            if not stack or stack.pop() != mapping[c]:
                return False
        else:
            stack.append(c)

    return len(stack) == 0

# Sample usage
print(is_valid_parentheses("()[]{}"))   # True
print(is_valid_parentheses("(]"))       # False


# ============================================================
# 2. MIN STACK (TRACK MINIMUM)
# ============================================================

class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def get_min(self):
        return self.min_stack[-1]

# Sample usage
ms = MinStack()
ms.push(3)
ms.push(1)
ms.push(2)
print(ms.get_min())  # 1
ms.pop()
print(ms.get_min())  # 1


# ============================================================
# 3. MONOTONIC STACK (NEXT GREATER ELEMENT)
# ============================================================

def next_greater(nums):
    res = [-1] * len(nums)
    stack = []  # store indices

    for i in range(len(nums)):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            res[idx] = nums[i]
        stack.append(i)

    return res

# Sample usage
print(next_greater([2, 1, 2, 4, 3]))  # [4, 2, 4, -1, -1]


# ============================================================
# QUEUE (FIFO - First In, First Out)
# ============================================================

q = deque()

# Enqueue (O(1))
q.append(5)
q.append(6)

# Dequeue (O(1))
print(q.popleft())   # 5
print(q)             # deque([6])


# ============================================================
# 4. IMPLEMENT QUEUE USING LIST (NOT IDEAL)
# ============================================================

def queue_with_list():
    q = []
    q.append(1)
    q.append(2)
    print(q.pop(0))   # O(n) ⚠️ slow

# Sample usage
queue_with_list()


# ============================================================
# 5. BFS (QUEUE USAGE) 🔥
# ============================================================

def bfs(graph, start):
    visited = set()
    q = deque([start])

    while q:
        node = q.popleft()
        if node not in visited:
            print(node, end=" ")
            visited.add(node)
            for nei in graph[node]:
                q.append(nei)

# Sample usage
graph = {
    0: [1, 2],
    1: [2],
    2: [0, 3],
    3: [3]
}
bfs(graph, 0)   # 0 1 2 3
print()


# ============================================================
# 6. SLIDING WINDOW MAX (DEQUE) 🔥
# ============================================================

def max_sliding_window(nums, k):
    q = deque()
    res = []

    for i in range(len(nums)):
        # remove out-of-window
        if q and q[0] <= i - k:
            q.popleft()

        # maintain decreasing order
        while q and nums[q[-1]] < nums[i]:
            q.pop()

        q.append(i)

        if i >= k - 1:
            res.append(nums[q[0]])

    return res

# Sample usage
print(max_sliding_window([1,3,-1,-3,5,3,6,7], 3))
# [3, 3, 5, 5, 6, 7]''',
        "leetcode_examples": [
            {
                "id": "LC 682",
                "title": "Baseball Game",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "You are given a list of operations for a baseball game. Each operation is either a number, '+', 'D', or 'C'. Return the sum of all the scores on the record.",
                "approach": "Use a stack to keep track of the scores. For each operation, update the stack accordingly and return the sum of all elements in the stack.",
                "code": '''def calPoints(operations: List[str]) -> int:
    stk = []

    for op in operations:
        if op == "+":
            stk.append(stk[-1] + stk[-2])
        elif op == "D":
            stk.append(stk[-1] * 2)
        elif op == "C":
            stk.pop()
        else:
            stk.append(int(op))

    return sum(stk)'''
            },
            {
                "id": "LC 20",
                "title": "Valid Parentheses",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "You are given a string of parentheses. Determine if the string is valid.",
                "approach": "Use a stack to keep track of the opening parentheses. For each closing parenthesis, check if it matches the most recent opening parenthesis.",
                "code": '''def isValid(s: str) -> bool:
    hashmap = {")": "(", "}": "{", "]": "["}
    stk = []

    for c in s:
        if c not in hashmap:
            stk.append(c)
        else:
            if not stk:
                return False
            else:
                popped = stk.pop()
                if popped != hashmap[c]:
                    return False

    return not stk'''
            },
            {
                "id": "LC 150",
                "title": "Evaluate Reverse Polish Notation (RPN) ",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "You are given a list of tokens representing an arithmetic expression in Reverse Polish Notation. Evaluate the expression and return the result.",
                "approach": "Use a stack to keep track of the operands. For each operator, pop the top two operands from the stack, perform the operation, and push the result back onto the stack.",
                "code": '''def evalRPN(tokens: List[str]) -> int:
    stk = []
    for t in tokens:
        if t in "+-*/":
            b, a = stk.pop(), stk.pop()

            if t == "+":
                stk.append(a + b)
            elif t == "-":
                stk.append(a - b)
            elif t == "*":
                stk.append(a * b)
            else:
                division = a / b
                if division < 0:
                    stk.append(ceil(division))
                else:
                    stk.append(floor(division))
        else:
            stk.append(int(t))

    return stk[0]'''
            },
            {
                "id": "LC 739",
                "title": "Daily Temperatures",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "You are given a list of daily temperatures. Return a list where each element is the number of days you have to wait after the ith day to get a warmer temperature.",
                "approach": "Use a stack to keep track of indices of temperatures. For each temperature, pop indices from the stack if the current temperature is warmer, and update the answer for those indices.",
                "code": '''def dailyTemperatures( temperatures: List[int]) -> List[int]:
    temps = temperatures
    n = len(temps)
    answer = [0] * n
    stk = []

    for i, t in enumerate(temps):
        while stk and stk[-1][0] < t:
            stk_t, stk_i = stk.pop()
            answer[stk_i] = i - stk_i

        stk.append((t, i))
    return answer'''
            },

            {
                "id": "LC 155",
                "title": "Min Stack",
                "difficulty": "Medium",
                "complexity": "O(1) time, O(n) space",
                "description": "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.",
                "approach": "Use two stacks: one for the actual stack and another to keep track of the minimum values. When pushing a new value, compare it with the current minimum and update the minimum stack accordingly.",
                "code": '''class MinStack:
    def __init__(self):
        self.stk = []
        self.min_stk = []
 
    def push(self, val: int) -> None:
        self.stk.append(val)
        if not self.min_stk:
            self.min_stk.append(val)
        elif self.min_stk[-1] < val:
            self.min_stk.append(self.min_stk[-1])
        else:
            self.min_stk.append(val)
 
    def pop(self) -> None:
        self.stk.pop()
        self.min_stk.pop()
 
    def top(self) -> int:
        return self.stk[-1]
 
    def getMin(self) -> int:
        return self.min_stk[-1]'''
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

class LinkedList:
    def __init__(self):
        self.head = None

    # Insert at the end
    def append(self, val):
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    # Insert at the beginning
    def prepend(self, val):
        self.head = ListNode(val, self.head)

    # Delete first occurrence of value
    def delete(self, val):
        curr = self.head
        prev = None
        while curr:
            if curr.val == val:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                return True  # Deleted successfully
            prev = curr
            curr = curr.next
        return False  # Value not found

    # Reverse the linked list
    def reverse(self):
        prev = None
        curr = self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    # Print all nodes
    def print_list(self):
        curr = self.head
        while curr:
            print(curr.val, end=" -> ")
            curr = curr.next
        print("None")

    # Find a value
    def find(self, val):
        curr = self.head
        while curr:
            if curr.val == val:
                return curr
            curr = curr.next
        return None

# Example usage
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.print_list()  # 1 -> 2 -> 3 -> None

ll.reverse()
ll.print_list()  # 3 -> 2 -> 1 -> None

ll.prepend(0)
ll.print_list()  # 0 -> 3 -> 2 -> 1 -> None

ll.delete(2)
ll.print_list()  # 0 -> 3 -> 1 -> None

node = ll.find(3)
print("Found:", node.val if node else "Not found")  # Found: 3''',
        "leetcode_examples": [
            {
                "id": "LC 83",
                "title": "Remove Duplicates from Sorted List",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Given the head of a sorted linked list, delete all duplicates such that each element appears only once.",
                "approach": "Use two pointers to traverse the list and remove duplicate nodes in-place.",
                "code": '''def deleteDuplicates(head: Optional[ListNode]) -> Optional[ListNode]:
    cur = head

    while cur and cur.next:
        if cur.val == cur.next.val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head'''
            },
            {
                "id": "LC 206",
                "title": "Reverse Linked List",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Given the head of a linked list, reverse the list and return the new head.",
                "approach": "Use three pointers to reverse the links in the list.",
                "code": '''def reverseList(head: Optional[ListNode]) -> Optional[ListNode]:
    cur = head
    prev = None
    
    while cur:
        temp = cur.next
        cur.next = prev
        prev = cur
        cur = temp
    
    return prev'''
            },
            {
                "id": "LC 21",
                "title": "Merge Two Sorted Lists",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Given the heads of two sorted linked lists, merge them into one sorted list.",
                "approach": "Use a dummy node and two pointers to traverse both lists and merge them in sorted order.",
                "code": '''def mergeTwoLists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    d = ListNode()
    cur = d

    while list1 and list2:
        if list1.val < list2.val:
            cur.next = list1
            cur = list1
            list1 = list1.next
        else:
            cur.next = list2
            cur = list2
            list2 = list2.next

    cur.next = list1 if list1 else list2

    return d.next'''
            },

            {
                "id": "LC 141",
                "title": "Linked List Cycle",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Given the head of a linked list, determine if the linked list has a cycle in it.",
                "approach": "Use the Floyd's Tortoise and Hare algorithm (two pointers) to detect if there's a cycle in the list.",
                "code": '''def hasCycle(head: Optional[ListNode]) -> bool:
    slow = fast = head

    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next

        if slow is fast:
            return True

    return False'''
            },
            {
                "id": "LC 876",
                "title": "Middle of the Linked List",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Given the head of a linked list, return the middle node of the linked list.",
                "approach": "Use the Floyd's Tortoise and Hare algorithm (two pointers) to find the middle node.",
                "code": '''def middleNode(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = head
    fast = head

    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next

    return slow'''
            },

            {
                "id": "LC 19",
                "title": "Remove Nth Node From End of List",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Given the head of a linked list and a position n, remove the nth node from the end of the list.",
                "approach": "Use two pointers to traverse the list and find the node to remove.",
                "code": '''def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    dummy = ListNode()
    dummy.next = head
    behind = ahead = dummy

    for _ in range(n + 1):
        ahead = ahead.next

    while ahead:
        behind = behind.next
        ahead = ahead.next

    behind.next = behind.next.next

    return dummy.next'''
            },

            {
                "id": "LC 138",
                "title": "Copy List with Random Pointer",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "Given the head of a linked list with random pointers, create a deep copy of the list.",
                "approach": "Use a hash map to store the mapping between original and copied nodes.",
                "code": '''def copyRandomList(head: "Optional [Node]") -> "Optional [Node]":
    if not head:
        return None

    curr = head
    old_to_new = {}

    while curr:
        node = Node(x=curr.val)
        old_to_new[curr] = node
        curr = curr.next

    curr = head

    while curr:
        new_node = old_to_new[curr]
        new_node.next = old_to_new[curr.next] if curr.next else None
        new_node.random = old_to_new[curr.random] if curr.random else None
        curr = curr.next

    return old_to_new[head]'''
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
        "python_code": '''# Iterative binary search
def binary_search(arr, target):
    """
    Standard iterative binary search.
    Returns True if target exists, else False.
    """
    L, R = 0, len(arr) - 1
    while L <= R:
        M = (L + R) // 2
        if arr[M] == target:
            return True
        elif arr[M] < target:
            L = M + 1
        else:
            R = M - 1
    return False

# Iterative binary search returning index
def binary_search_index(arr, target):
    """
    Returns the index of the target if found, else -1.
    """
    L, R = 0, len(arr) - 1
    while L <= R:
        M = (L + R) // 2
        if arr[M] == target:
            return M
        elif arr[M] < target:
            L = M + 1
        else:
            R = M - 1
    return -1

# Recursive binary search
def binary_search_recursive(arr, target, L=0, R=None):
    """
    Recursive binary search.
    Returns True if target exists, else False.
    """
    if R is None:
        R = len(arr) - 1
    if L > R:
        return False
    M = (L + R) // 2
    if arr[M] == target:
        return True
    elif arr[M] < target:
        return binary_search_recursive(arr, target, M + 1, R)
    else:
        return binary_search_recursive(arr, target, L, M - 1)

# Find first and last occurrence (for arrays with duplicates)
def binary_search_bounds(arr, target):
    """
    Returns (first_index, last_index) of target in sorted array.
    Returns (-1, -1) if not found.
    """
    def find_first():
        L, R = 0, len(arr) - 1
        first = -1
        while L <= R:
            M = (L + R) // 2
            if arr[M] == target:
                first = M
                R = M - 1  # search left
            elif arr[M] < target:
                L = M + 1
            else:
                R = M - 1
        return first

    def find_last():
        L, R = 0, len(arr) - 1
        last = -1
        while L <= R:
            M = (L + R) // 2
            if arr[M] == target:
                last = M
                L = M + 1  # search right
            elif arr[M] < target:
                L = M + 1
            else:
                R = M - 1
        return last

    return find_first(), find_last()

# Example usage
arr = [1, 2, 3, 3, 3, 4, 5]
print(binary_search(arr, 3))             # True
print(binary_search_index(arr, 3))       # 2 (first found index)
print(binary_search_recursive(arr, 4))   # True
print(binary_search_bounds(arr, 3))      # (2, 4) first and last occurrence
print(binary_search_bounds(arr, 6))      # (-1, -1)''',
        "leetcode_examples": [
            {
                "id": "LC 704",
                "title": "Binary Search",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Given a sorted array of integers and a target value, return the index of the target if it exists, otherwise return -1.",
                "approach": "Use binary search to efficiently find the target in the sorted array.",
                "code": '''def search(nums: List[int], target: int) -> int:
    n = len(nums)
    for i in range(n):
        if nums[i] == target:
            return i
    return -1'''
            },

            {
                "id": "LC 35",
                "title": "Search Insert Position",
                "difficulty": "Easy",
                "complexity": "O(log n) time, O(1) space",
                "description": "Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.",
                "approach": "Use binary search to find the target or determine its insertion point.",
                "code": '''def searchInsert(nums: List[int], target: int) -> int:
    n = len(nums)
    l = 0
    r = n - 1

    while l <= r:
        m = (l + r) // 2
        
        if nums[m] < target:
            l = m + 1
        elif nums[m] > target:
            r = m - 1
        else:
            return m

    if nums[m] < target:
        return m + 1
    else:
        return m'''
            },


            {
                "id": "LC 278",
                "title": "First Bad Version",
                "difficulty": "Easy",
                "complexity": "O(log n) time, O(1) space",
                "description": "You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.",
                "approach": "Use binary search to efficiently find the first bad version.",
                "code": '''def firstBadVersion(self, n: int) -> int:
    L = 1
    R = n

    while L < R:
        M = (L+R) // 2
        if isBadVersion(M):
            R = M
        else:
            L = M + 1
    
    return L '''
            },

            {
                "id": "LC 367",
                "title": "Valid Perfect Square",
                "difficulty": "Easy",
                "complexity": "O(log n) time, O(1) space",
                "description": "Given a positive integer num, write a function to determine if it is a perfect square.",
                "approach": "Use binary search to efficiently find if there exists an integer whose square equals the given number.",
                "code": '''def isPerfectSquare(num: int) -> bool:
    l = 1
    r = num

    while l <= r:
        m = (l+r) // 2
        m_squared = m * m

        if num == m_squared:
            return True
        elif m_squared < num:
            l = m + 1
        else:
            r = m - 1
    
    return False'''
            },

            {
                "id": "LC 74",
                "title": "Search a 2D Matrix",
                "difficulty": "Medium",
                "complexity": "O(log(m * n)) time, O(1) space",
                "description": "Write an efficient algorithm that searches for a value target in an m x n integer matrix.",
                "approach": "Treat the 2D matrix as a 1D array and use binary search.",
                "code": '''def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m = len(matrix)
        n = len(matrix[0])
        t = m * n
        l = 0
        r = t - 1
 
        while l <= r:
            mid = (l + r) // 2
            mid_i = mid // n
            mid_j = mid % n
            mid_num = matrix[mid_i][mid_j]
 
            if target == mid_num:
                return True
            elif target < mid_num:
                r = mid - 1
            else:
                l = mid + 1
 
        return False'''
            },

            {
                "id": "LC 153",
                "title": "Find Minimum in Rotated Sorted Array",
                "difficulty": "Medium",
                "complexity": "O(log(n)) time, O(1) space",
                "description": "Given a sorted array of unique elements that has been rotated at some pivot unknown to you beforehand, find the minimum element.",
                "approach": "Use binary search to find the minimum element in the rotated sorted array.",
                "code": '''def findMin(nums: List[int]) -> int:
    n = len(nums)
    l = 0
    r = n - 1

    while l < r:
        m = (l + r) // 2
    
        if nums[m] > nums[r]:
            l = m + 1
        else:
            r = m

    return nums[l]'''
            },

            {
                "id": "LC 33",
                "title": "Search in Rotated Sorted Array",
                "difficulty": "Medium",
                "complexity": "O(log(n)) time, O(1) space",
                "description": "Given a sorted array of unique elements that has been rotated at some pivot unknown to you beforehand, search for a target value.",
                "approach": "Use binary search to find the target value in the rotated sorted array.",
                "code": '''def search(nums: List[int], target: int) -> int:
        n = len(nums)
        l = 0
        r = n - 1
 
        while l < r:
            m = (l + r) // 2
 
            if nums[m] > nums[r]:
                l = m + 1
            else:
                r = m
 
        min_i = l
 
        if min_i == 0:
            l, r = 0, n - 1
        elif target >= nums[0] and target <= nums[min_i - 1]:
            l, r = 0, min_i - 1
        else:
            l, r = min_i, n - 1
 
        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                return m
            elif nums[m] < target:
                l = m + 1
            else:
                r = m - 1
        return -1'''
            },


            {
                "id": "LC 875",
                "title": "Koko Eating Bananas",
                "difficulty": "Medium",
                "complexity": "O(n * log(m)) time, O(1) space",
                "description": "Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.",
                "approach": "Use binary search to find the minimum eating speed.",
                "code": '''def minEatingSpeed(piles: List[int], h: int) -> int:
    def k_works(k):
        hours = 0

        for p in piles:
            hours += ceil(p / k)

        return hours <= h

    l = 1
    r = max(piles) # m

    while l < r:
        k = (l + r) // 2

        if k_works(k):
            r = k
        else:
            l = k + 1

    return r'''
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
        "python_code": '''# ----------------------------
# Sliding Window Utilities
# ----------------------------

# Fixed window: max sum of k consecutive elements
def max_sum_k(arr, k):
    """
    Returns the maximum sum of any contiguous subarray of size k.
    """
    if k > len(arr) or k <= 0:
        return None
    window_sum = sum(arr[:k])
    best = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        best = max(best, window_sum)
    return best

# Fixed window: min sum of k consecutive elements
def min_sum_k(arr, k):
    """
    Returns the minimum sum of any contiguous subarray of size k.
    """
    if k > len(arr) or k <= 0:
        return None
    window_sum = sum(arr[:k])
    best = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        best = min(best, window_sum)
    return best

# Variable window: longest substring with all unique characters
def longest_unique_substring(s):
    """
    Returns the length of the longest substring with all unique characters.
    """
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

# Variable window: smallest subarray with sum >= target
def min_subarray_sum(arr, target):
    """
    Returns the length of the smallest contiguous subarray with sum >= target.
    Returns 0 if no such subarray exists.
    """
    L = 0
    curr_sum = 0
    best = float('inf')
    for R in range(len(arr)):
        curr_sum += arr[R]
        while curr_sum >= target:
            best = min(best, R - L + 1)
            curr_sum -= arr[L]
            L += 1
    return 0 if best == float('inf') else best

# Example usage
arr = [2, 1, 5, 1, 3, 2]
print("Max sum of 3 consecutive elements:", max_sum_k(arr, 3))    # 9
print("Min sum of 2 consecutive elements:", min_sum_k(arr, 2))    # 2

s = "abcabcbb"
print("Longest unique substring length:", longest_unique_substring(s))  # 3

arr2 = [2,3,1,2,4,3]
target = 7
print("Min subarray length with sum >= 7:", min_subarray_sum(arr2, target))  # 2''',
        "leetcode_examples": [
            {
                "id": "LC 643",
                "title": "Maximum Average Subarray I",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(1) space",
                "description": "Given an array of integers and a window size k, find the maximum average of any subarray of size k.",
                "approach": "Use a sliding window approach to calculate the sum of each subarray of size k and keep track of the maximum sum.",
                "code": '''def findMaxAverage(nums: List[int], k: int) -> float:
    n = len(nums)
    cur_sum = 0

    for i in range(k):
        cur_sum += nums[i]

    max_avg = cur_sum / k

    for i in range(k, n):
        cur_sum += nums[i]
        cur_sum -= nums[i - k]

        avg = cur_sum / k
        max_avg = max(max_avg, avg)

    return max_avg'''
            },


            {
                "id": "LC 1004",
                "title": "Max Consecutive Ones III",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Given a binary array and an integer k, find the maximum number of consecutive 1s in the array if you can flip at most k 0s to 1s.",
                "approach": "Use a sliding window approach to keep track of the number of zeros in the current window. If the number of zeros exceeds k, move the left pointer until the number of zeros is at most k again.",
                "code": '''def longestOnes(nums: List[int], k: int) -> int:
    max_w = 0
    num_zeros = 0
    n = len(nums)
    l = 0

    for r in range(n):
        if nums[r] == 0:
            num_zeros += 1

        while num_zeros > k:
            if nums[l] == 0:
                num_zeros -= 1
            l += 1
        w = r - l + 1
        max_w = max(max_w, w)

    return max_w'''
            },


            {
                "id": "LC 3",
                "title": "Longest Substring Without Repeating Characters",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "Given a string, find the length of the longest substring without repeating characters.",
                "approach": "Use a sliding window approach to keep track of the characters in the current window. If a repeated character is found, move the left pointer until the character is no longer in the window.",
                "code": '''def lengthOfLongestSubstring(s: str) -> int:
    l = 0
    longest = 0
    sett = set()
    n = len(s)

    for r in range(n):
        while s[r] in sett:
            sett.remove(s[l])
            l += 1

        w = (r - l) + 1
        longest = max(longest, w)
        sett.add(s[r])

    return longest'''
            },

            {
                "id": "LC 424",
                "title": "Longest Repeating Character Replacement",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Given a string and an integer k, find the length of the longest substring that can be made by replacing at most k characters with any other character.",
                "approach": "Use a sliding window approach to keep track of the characters in the current window. If the number of characters that need to be replaced exceeds k, move the left pointer until the number of replacements is at most k again.",
                "code": '''def characterReplacement(s: str, k: int) -> int:
    longest = 0
    l = 0
    counts = [0] * 26

    for r in range(len(s)):
        counts[ord(s[r]) - 65] += 1

        while (r - l + 1) - max(counts) > k:
            counts[ord(s[l]) - 65] -= 1
            l += 1

        longest = max(longest, (r - l + 1))

    return longest'''
            },

            {
                "id": "LC 209",
                "title": "Minimum Size Subarray Sum",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Given an array of positive integers and a target sum, find the minimal length of a contiguous subarray whose sum is greater than or equal to the target.",
                "approach": "Use a sliding window approach to keep track of the current subarray sum. If the sum is greater than or equal to the target, update the minimum length and move the left pointer.",
                "code": '''def minSubArrayLen(target: int, nums: List[int]) -> int:
    min_length = float('inf')
    summ = 0
    l = 0
    
    for r in range(len(nums)):
        summ += nums[r]
        while summ >= target:
            min_length = min(min_length, r-l+1)
            summ -= nums[l]
            l += 1
    
    return min_length if min_length < float('inf') else 0'''
            },

            {
                "id": "LC 587",
                "title": "Permutation in String",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Given two strings s1 and s2, determine if s2 contains a permutation of s1 as a substring.",
                "approach": "Use a sliding window approach to keep track of the characters in the current window. If the window contains a permutation of s1, return True.",
                "code": '''def checkInclusion(s1: str, s2: str) -> bool:
    n1 = len(s1)
    n2 = len(s2)

    if n1 > n2:
        return False

    s1_counts = [0] * 26
    s2_counts = [0] * 26

    for i in range(n1):
        s1_counts[ord(s1[i]) - 97] += 1
        s2_counts[ord(s2[i]) - 97] += 1

    if s1_counts == s2_counts:
        return True

    for i in range(n1, n2):
        s2_counts[ord(s2[i]) - 97] += 1
        s2_counts[ord(s2[i - n1]) - ord("a")] -= 1
        if s1_counts == s2_counts:
            return True

    return False'''
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
                "id": "LC 225",
                "title": "Invert Binary Tree",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(h) space",
                "description": "Invert a binary tree.",
                "approach": "Recursively swap the left and right children of each node.",
                "code": '''def invertTree(root: Optional[TreeNode]) -> Optional[TreeNode]:

    if not root:
        return None

    root.left, root.right = root.right, root.left

    self.invertTree(root.left)
    self.invertTree(root.right)

    return root'''
            },

            {
                "id": "LC 104",
                "title": "Maximum Depth of Binary Tree",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(h) space",
                "description": "Find the maximum depth of a binary tree.",
                "approach": "Recursively calculate the depth of the left and right subtrees and return the maximum.",
                "code": '''def maxDepth(root: Optional[TreeNode]) -> int:
    if not root:
        return 0

    left = self.maxDepth(root.left)
    right = self.maxDepth(root.right)

    return 1 + max(left, right)'''
            },


            {
                "id": "LC 110",
                "title": "Balanced Binary Tree",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(h) space",
                "description": "Determine if a binary tree is height-balanced.",
                "approach": "Recursively check if the left and right subtrees are balanced and their heights differ by at most 1.",
                "code": '''def isBalanced(root: Optional[TreeNode]) -> bool:
    balanced = [True]

    def height(root):
        if not root:
            return 0

        left_height = height(root.left)
        if balanced[0] is False:
            return 0


        right_height = height(root.right)
        if abs(left_height - right_height) > 1:
            balanced[0] = False
            return 0
        return 1 + max(left_height, right_height)

    height(root)
    return balanced[0]'''
            },

            {
                "id": "LC 543",
                "title": "Diameter of Binary Tree",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(h) space",
                "description": "Find the diameter of a binary tree, which is the length of the longest path between any two nodes in the tree.",
                "approach": "Recursively calculate the height of the left and right subtrees while updating the diameter at each node.",
                "code": '''def diameterOfBinaryTree(root: Optional[TreeNode]) -> int:
    largest_diameter = [0]

    def height(root):
        if root is None:
            return 0

        left_height = height(root.left)
        right_height = height(root.right)
        diameter = left_height + right_height

        largest_diameter[0] = max(largest_diameter[0], diameter)
        
        return 1 + max(left_height, right_height)

    height(root)
    return largest_diameter[0]'''
            },

            {
                "id": "LC 100",
                "title": "Same Binary Tree",
                "difficulty": "Easy",
                "complexity": "O(n + m) time, O(n + m) space",
                "description": "Determine if two binary trees are the same.",
                "approach": "Recursively compare the values of corresponding nodes in both trees.",
                "code": '''def isSameTree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    # 1: Both Null
    if not p and not q: 
        return True
    
    # 2: One is Null
    if (p and not q) or (q and not p):
        return False
    
    # 3. Values Mismatch
    if p.val != q.val:
        return False
    
    return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)'''
            },

            {
                "id": "LC 101",
                "title": "Symmetric Tree",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Determine if a binary tree is symmetric.",
                "approach": "Recursively compare the left and right subtrees of the root.",
                "code": '''def isSymmetric(root: Optional[TreeNode]) -> bool:
        def same(root1, root2):
            if not root1 and not root2:
                return True
 
            if not root1 or not root2:
                return False
            
            if root1.val != root2.val:
                return False
            
            return same(root1.left, root2.right) and same(root1.right, root2.left)
 
        return same(root, root)'''
            },

            {
                "id": "LC 112",
                "title": "Path Sum",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(h) space",
                "description": "Determine if a binary tree has a root-to-leaf path such that adding up all the values along the path equals a given sum.",
                "approach": "Recursively calculate the sum of the values along the path from the root to each leaf node and check if it equals the target sum.",
                "code": '''def hasPathSum(root: Optional[TreeNode], targetSum: int) -> bool:
 
    def has_sum(root, cur_sum):
        if not root:
            return False

        cur_sum += root.val

        if not root.left and not root.right:
            return cur_sum == targetSum
        
        return has_sum(root.left, cur_sum) or  has_sum(root.right, cur_sum)
    
    return has_sum(root, 0)'''
            },

            {
                "id": "LC 150",
                "title": "Minimum Absolute Difference in BST",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(h) space",
                "description": "Find the minimum absolute difference between the values of any two different nodes in a BST.",
                "approach": "Perform an in-order traversal of the BST and keep track of the previous node's value to calculate the difference.",
                "code": '''def getMinimumDifference(root: Optional[TreeNode]) -> int:
    min_distance = [float('inf')]
    prev = [None]

    def dfs(node):
        if node is None:
            return
            
        dfs(node.left)

        if prev[0] is not None:
            min_distance[0] = min(min_distance[0], node.val - prev[0])

        prev[0] = node.val
        dfs(node.right)

    dfs(root)
    return min_distance[0]'''
            },

            {
                "id": "LC 572",
                "title": "Subtree of Another Tree",
                "difficulty": "Medium",
                "complexity": "O(m * n) time, O(n) space",
                "description": "Determine if a binary tree is a subtree of another binary tree.",
                "approach": "Recursively check if the current node and its subtrees match the subtree rooted at subRoot.",
                "code": '''def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
 
        def sameTree(p, q):
            if not p and not q:
                return True
 
            if (p and not q) or (q and not p):
                return False
 
            if p.val != q.val:
                return False
 
            return sameTree(p.left, q.left) and sameTree(p.right, q.right)
 
        def has_subtree(root):
            if not root:
                return False
 
            if sameTree(root, subRoot):
                return True
            
            return has_subtree(root.left) or has_subtree(root.right)
 
        return has_subtree(root)'''
            },

            {
                "id": "LC 102",
                "title": "Binary Tree Level Order Traversal (BFS)",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "Return the level order traversal of a binary tree's nodes' values.",
                "approach": "Use a queue to perform a breadth-first search and collect nodes level by level.",
                "code": '''def levelOrder(root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return None
        
        queue = deque()
        queue.append(root)
        ans = []
        
        while queue:
            level = []
            n = len(queue)
            for i in range(n):
                node = queue.popleft()
                level.append(node.val)
 
                if node.left: queue.append(node.left)                
                if node.right: queue.append(node.right)
            
            ans.append(level)
 
        return ans'''
            },

            {
                "id": "LC 230",
                "title": "Kth Smallest Element in a BST",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "Find the kth smallest element in a BST.",
                "approach": "Perform an in-order traversal and stop when the kth element is found.",
                "code": '''def kthSmallest(root: Optional[TreeNode], k: int) -> int:
    count = [k]
    ans = [0]

    def dfs(node):
        if not node:
            return
        
        dfs(node.left)

        if count[0] == 1:
            ans[0] = node.val
        
        count[0] = count[0] - 1
        if count[0] > 0:
            dfs(node.right)
    
    dfs(root)
    return ans[0]'''
            },

            {
                "id": "LC 98",
                "title": "Validate Binary Search Tree",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(n) space",
                "description": "Validate if a binary tree is a valid binary search tree.",
                "approach": "Perform a recursive check ensuring each node's value is within the valid range.",
                "code": '''def isValidBST(self, root: Optional[TreeNode]) -> bool:
    def is_valid(node, minn, maxx):
        if not node:
            return True
        
        if node.val <= minn or node.val >= maxx:
            return False
        
        return is_valid(node.left, minn, node.val) and is_valid(node.right, node.val, maxx)

    return is_valid(root, float("-inf"), float("inf"))'''
            },

            {
                "id": "LC 235",
                "title": "Lowest Common Ancestor of a Binary Search Tree",
                "difficulty": "Medium",
                "complexity": "O(h) time, O(h) space",
                "description": "Find the lowest common ancestor of two nodes in a binary search tree.",
                "approach": "Use the properties of a binary search tree to navigate towards the nodes and find their common ancestor.",
                "code": '''def lowestCommonAncestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    lca = [root]

    def search(root):
        if not root:
            return

        lca[0] = root
        if root is p or root is q:
            return
        elif root.val < p.val and root.val < q.val:
            search(root.right)
        elif root.val > p.val and root.val > q.val:
            search(root.left)
        else:
            return

    search(root)
    return lca[0]'''
            },

            {
                "id": "LC 208",
                "title": "Implement Trie (Prefix Tree)",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(T) space",
                "description": "Implement a trie (prefix tree) data structure.",
                "approach": "Use a dictionary to represent nodes and track the end of words.",
                "code": '''	class Trie:
    def __init__(self):
        self.trie = {}
 
    def insert(self, word: str) -> None:
        d = self.trie
 
        for c in word:
            if c not in d:
                d[c] = {}
            d = d[c]
 
        d['.'] = '.'
 
    def search(self, word: str) -> bool:
        d = self.trie
 
        for c in word:
            if c not in d:
                return False
            d = d[c]
 
        return '.' in d
 
    def startsWith(self, prefix: str) -> bool:
        d = self.trie
 
        for c in prefix:
            if c not in d:
                return False
            d = d[c]
 
        return True'''
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

# ----------------------------
# Heap Utilities
# ----------------------------

class MinHeap:
    def __init__(self, arr=None):
        """
        Initialize min-heap from array (optional)
        """
        self.heap = arr[:] if arr else []
        if self.heap:
            heapq.heapify(self.heap)

    def push(self, val):
        heapq.heappush(self.heap, val)

    def pop(self):
        return heapq.heappop(self.heap) if self.heap else None

    def peek(self):
        return self.heap[0] if self.heap else None

    def __len__(self):
        return len(self.heap)

class MaxHeap:
    def __init__(self, arr=None):
        """
        Initialize max-heap using negation
        """
        self.heap = [-x for x in arr] if arr else []
        if self.heap:
            heapq.heapify(self.heap)

    def push(self, val):
        heapq.heappush(self.heap, -val)

    def pop(self):
        return -heapq.heappop(self.heap) if self.heap else None

    def peek(self):
        return -self.heap[0] if self.heap else None

    def __len__(self):
        return len(self.heap)

# ----------------------------
# Example Usage
# ----------------------------

# Min-Heap
min_heap = MinHeap([-4, 3, 1, 0, 2, 5])
print("Min-Heap peek:", min_heap.peek())  # -4
print("Min-Heap pop:", min_heap.pop())    # -4
min_heap.push(-10)
print("Min-Heap peek after push:", min_heap.peek())  # -10

# Max-Heap
max_heap = MaxHeap([9, 1, 5])
print("Max-Heap peek:", max_heap.peek())  # 9
print("Max-Heap pop:", max_heap.pop())    # 9
max_heap.push(20)
print("Max-Heap peek after push:", max_heap.peek())  # 20''',
        "leetcode_examples": [
            {
                "id": "LC 1046",
                "title": "Last Stone Weight",
                "difficulty": "Easy",
                "complexity": "O(n log n) time, O(1) space",
                "description": "You are given an array of integers `stones` where `stones[i]` is the weight of the `i`-th stone. We are playing a game with the stones. On each turn, we choose the heaviest two stones",
                "approach": "1. Negate the weights to use a Min Heap as a Max Heap.\n2. Use `heapq` to create a Min Heap from the negated weights.\n3. While there are more than one stone, pop the two heaviest stones (the smallest in the Min Heap), compare them, and if they are not equal, push the difference back into the heap.\n4. Finally, return the weight of the last remaining stone (negate it back to get the original weight) or 0 if there are no stones left.",
                "code": '''def lastStoneWeight(stones: List[int]) -> int:
    for i in range(len(stones)):
        stones[i] *= -1 # Negate to force Max Heap

    heapq.heapify(stones)

    while len(stones) > 1:
        largest = heapq.heappop(stones)
        next_largest = heapq.heappop(stones)

        if largest != next_largest:
            heapq.heappush(stones, largest - next_largest)

    return -heapq.heappop(stones) if stones else 0'''
            },

            {
                "id": "LC 215",
                "title": "Kth Largest Element in an Array",
                "difficulty": "Medium",
                "complexity": " O(n + k log n) time, O(1) space",
                "description": "You are given an array of integers `nums` and an integer `k`. Return the kth largest element in the array.",
                "approach": "1. Negate the elements of the array to use a Min Heap as a Max Heap.\n2. Use `heapq` to create a Min Heap from the negated elements.\n3. Pop the smallest element (the largest in the original array) from the heap `k-1` times.\n4. Finally, return the next popped element (negate it back to get the original value) as the kth largest element.",
                "code": '''import heapq
def findKthLargest(self, nums: List[int], k: int) -> int:
    for i in range(len(nums)):
        nums[i] = -nums[i] # Max Heap

    heapq.heapify(nums)

    for _ in range(k-1):
        heapq.heappop(nums)

    return -heapq.heappop(nums)'''
            },

            {
                "id": "LC 347",
                "title": "Top K Frequent Elements",
                "difficulty": "Medium",
                "complexity": " O(n log k) time, O(k) space",
                "description": "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.",
                "approach": "1. Count the frequency of each element.\n2. Use a Min Heap to keep track of the top k frequent elements.\n3. Pop the smallest element (the least frequent in the heap) from the heap `k-1` times.\n4. Finally, return the next popped element as the kth most frequent element.",
                "code": '''from collections import Counter
import heapq

def topKFrequent(nums: List[int], k: int) -> List[int]:
    counter = Counter(nums)
    heap = []

    for key, val in counter.items():
        if len(heap) < k:
            heapq.heappush(heap, (val, key))
        else:
            heapq.heappushpop(heap, (val, key))
    
    return [h[1] for h in heap]'''
            },

            {
                "id": "LC 973",
                "title": "K Closest Points to Origin",
                "difficulty": "Medium",
                "complexity": " O(n log k) time, O(k) space",
                "description": "Given an array of points on the X-Y plane and an integer `k`, return the `k` closest points to the origin (0, 0).",
                "approach": "1. Calculate the distance of each point from the origin using the formula `dist = x^2 + y^2`.\n2. Use a Max Heap to keep track of the k closest points.\n3. For each point, if the heap has less than k points, push it onto the heap. Otherwise, compare the distance of the current point with the largest distance in the heap (the root). If the current point is closer, replace the root with the current point.\n4. Finally, return the points in the heap as the k closest points.",
                "code": '''def kClosest(points: List[List[int]], k: int) -> List[List[int]]:
    def dist(x, y):
        return x**2 + y**2

    heap = []
    for x, y in points:
        d = dist(x, y)
        if len(heap) < k:
            heapq.heappush(heap, (-d, x, y))
        else:
            heapq.heappushpop(heap, (-d, x, y))

    return [(x, y) for d, x, y in heap]'''
            },

            {
                "id": "LC 23",
                "title": "Merge K Sorted Linked Lists",
                "difficulty": "Hard",
                "complexity": " O(N log K) time, O(k) space",
                "description": "Given an array of points on the X-Y plane and an integer `k`, return the `k` closest points to the origin (0, 0).",
                "approach": "1. Calculate the distance of each point from the origin using the formula `dist = x^2 + y^2`.\n2. Use a Max Heap to keep track of the k closest points.\n3. For each point, if the heap has less than k points, push it onto the heap. Otherwise, compare the distance of the current point with the largest distance in the heap (the root). If the current point is closer, replace the root with the current point.\n4. Finally, return the points in the heap as the k closest points.",
                "code": '''import heapq
def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    
    D = ListNode()
    cur = D
    
    # n log k
    while heap:
        val, i, node = heapq.heappop(heap)
        cur.next = node
        cur = node
        node = node.next
        if node:
            heapq.heappush(heap, (node.val, i, node))
    
    return D.next'''
            }
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
        "python_code": '''# Generate all subsets of a list
def subsets(nums):
    """
    Returns all possible subsets of nums
    """
    res = []
    sol = []

    def backtrack(i):
        if i == len(nums):
            res.append(sol.copy())
            return
        # Don't pick
        backtrack(i + 1)
        # Pick
        sol.append(nums[i])
        backtrack(i + 1)
        sol.pop()  # Undo

    backtrack(0)
    return res

# Generate all permutations of a list
def permutations(nums):
    """
    Returns all possible permutations of nums
    """
    res = []
    sol = []
    used = [False] * len(nums)

    def backtrack():
        if len(sol) == len(nums):
            res.append(sol.copy())
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            sol.append(nums[i])
            backtrack()
            sol.pop()
            used[i] = False

    backtrack()
    return res

# Combination sum (numbers can be reused)
def combination_sum(candidates, target):
    """
    Returns all unique combinations where numbers sum to target.
    Numbers can be reused.
    """
    res = []
    sol = []

    def backtrack(i, total):
        if total == target:
            res.append(sol.copy())
            return
        if total > target or i == len(candidates):
            return
        # Pick
        sol.append(candidates[i])
        backtrack(i, total + candidates[i])
        sol.pop()  # Undo
        # Don't pick
        backtrack(i + 1, total)

    backtrack(0, 0)
    return res

# N-Queens problem (return board positions)
def n_queens(n):
    """
    Returns all valid N-Queens arrangements as lists of column indices per row.
    """
    res = []
    sol = []

    def is_safe(row, col):
        for r, c in enumerate(sol):
            if c == col or abs(c - col) == row - r:
                return False
        return True

    def backtrack(row):
        if row == n:
            res.append(sol.copy())
            return
        for col in range(n):
            if is_safe(row, col):
                sol.append(col)
                backtrack(row + 1)
                sol.pop()

    backtrack(0)
    return res

# ----------------------------
# Example Usage
# ----------------------------

nums = [1, 2, 3]
print("Subsets:", subsets(nums))
print("Permutations:", permutations(nums))

candidates = [2, 3, 6, 7]
target = 7
print("Combination Sum:", combination_sum(candidates, target))

n = 4
print("4-Queens Solutions:", n_queens(n))''',
        "leetcode_examples": [
            {
                "id": "LC 78",
                "title": "Subsets",
                "difficulty": "Medium",
                "complexity": "O(2^n) time, O(n) space",
                "description": "Return all possible subsets of a given array.",
                "approach": "Use backtracking to generate all possible combinations.",
                "code": '''def subsets(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    ans, sol = [], []

    def backtrack(i):
        if i == n:
            ans.append(sol[:])
            return

        # Don't pick nums[i]
        backtrack(i + 1)

        # Pick nums[i]
        sol.append(nums[i])
        backtrack(i + 1)
        sol.pop()

    backtrack(0)
    return ans'''
            },

            {
                "id": "LC 46",
                "title": "Permutations",
                "difficulty": "Medium",
                "complexity": "O(n!) time, O(n) space",
                "description": "Return all possible permutations of a given array.",
                "approach": "Use backtracking to generate all possible arrangements.",
                "code": '''def permute(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    ans, sol = [], []

    def backtrack():
        if len(sol) == n:
            ans.append(sol[:])
            return

        for x in nums:
            if x not in sol:
                sol.append(x)
                backtrack()
                sol.pop()

    backtrack()
    return ans'''
            },

            {
                "id": "LC 77",
                "title": "Combinations",
                "difficulty": "Medium",
                "complexity": "O(n choose k) time, O(k) space",
                "description": "Return all possible combinations of k numbers chosen from the range [1, n].",
                "approach": "Use backtracking to generate all possible combinations.",
                "code": '''def combine(self, n: int, k: int) -> List[List[int]]:
    ans, sol = [], []

    def backtrack(x):
        if len(sol) == k:
            ans.append(sol[:])
            return

        left = x
        still_need = k - len(sol)

        if left > still_need:
            backtrack(x - 1)

        sol.append(x)
        backtrack(x - 1)
        sol.pop()

    backtrack(n)
    return ans'''
            },

            {
                "id": "LC 39",
                "title": "Combination Sum",
                "difficulty": "Medium",
                "complexity": "O(n**t) time, O(n) space",
                "description": "Return all possible combinations of candidates that sum to the target. Each number in candidates may be used an unlimited number of times.",
                "approach": "Use backtracking to generate all possible combinations while keeping track of the current sum.",
                "code": '''def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    res, sol = [], []
    nums = candidates
    n = len(nums)
    
    def backtrack(i, cur_sum):
        if cur_sum == target:
            res.append(sol[:])
            return
        
        if cur_sum > target or i == n:
            return

        backtrack(i+1, cur_sum)

        sol.append(nums[i])
        backtrack(i, cur_sum+nums[i])
        sol.pop()
    
    backtrack(0, 0)
    return res'''
            },

            {
                "id": "LC 17",
                "title": "Letter Combinations of a Phone Number",
                "difficulty": "Medium",
                "complexity": "O(n * 4^n) time, O(n) space",
                "description": "Return all possible letter combinations that the number could represent based on the mapping of digits to letters on a phone keypad.",
                "approach": "Use backtracking to generate all possible combinations while keeping track of the current index.",
                "code": '''def letterCombinations(digits: str) -> List[str]:
    if digits == "":
        return []

    ans, sol = [], []
    
    letter_map = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }
    
    n = len(digits)

    def backtrack(i=0):
        if i == n:
            ans.append("".join(sol))
            return

        for letter in letter_map[digits[i]]:
            sol.append(letter)
            backtrack(i + 1)
            sol.pop()

    backtrack(0)
    return ans'''
            },

            {
                "id": "LC 22",
                "title": "Generate Parentheses",
                "difficulty": "Medium",
                "complexity": "O(2^n) time, O(n) space",
                "description": "Return all possible combinations of well-formed parentheses.",
                "approach": "Use backtracking to generate all possible combinations while keeping track of the number of open and close parentheses.",
                "code": '''def generateParenthesis(n: int) -> List[str]:
    ans, sol = [], []

    def backtrack(openn, close):
        if len(sol) == 2 * n:
            ans.append("".join(sol))
            return
        if openn < n:
            sol.append("(")
            backtrack(openn + 1, close)
            sol.pop()

        if openn > close:
            sol.append(")")
            backtrack(openn, close + 1)
            sol.pop()

    backtrack(0, 0)
    return ans'''
            },

            {
                "id": "LC 79",
                "title": "Word Search",
                "difficulty": "Medium",
                "complexity": "O((m*n)^2) time, O(W) space",
                "description": "Return true if the word exists in the grid, false otherwise.",
                "approach": "Use backtracking to explore all possible paths in the grid while keeping track of the current position and the word being searched.",
                "code": '''def exist(board: List[List[str]], word: str) -> bool:
    m = len(board)
    n = len(board[0])
    W = len(word)

    if m == 1 and n == 1:
        return board[0][0] == word

    def backtrack(pos, index):
        i, j = pos

        if index == W:
            return True

        if board[i][j] != word[index]:
            return False

        char = board[i][j]
        board[i][j] = "#"

        for i_off, j_off in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            r, c = i + i_off, j + j_off

            if 0 <= r < m and 0 <= c < n:
                if backtrack((r, c), index + 1):
                    return True

        board[i][j] = char
        return False

    for i in range(m):
        for j in range(n):
            if backtrack((i, j), 0):
                return True

    return False'''
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

# ----------------------------
# Graph Utilities
# ----------------------------

class Graph:
    def __init__(self, edges=None, directed=False):
        """
        Initialize a graph from edges. Can be directed or undirected.
        """
        self.graph = defaultdict(list)
        self.directed = directed
        if edges:
            for u, v in edges:
                self.add_edge(u, v)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)

    # ----------------------------
    # Traversals
    # ----------------------------

    def bfs(self, start):
        """
        Breadth-first search starting from `start`.
        Returns the order of visited nodes.
        """
        seen = {start}
        q = deque([start])
        order = []
        while q:
            node = q.popleft()
            order.append(node)
            for nb in self.graph[node]:
                if nb not in seen:
                    seen.add(nb)
                    q.append(nb)
        return order

    def dfs(self, start):
        """
        Depth-first search starting from `start`.
        Returns the order of visited nodes.
        """
        seen = set()
        order = []

        def dfs_rec(node):
            seen.add(node)
            order.append(node)
            for nb in self.graph[node]:
                if nb not in seen:
                    dfs_rec(nb)

        dfs_rec(start)
        return order

    # ----------------------------
    # Utilities
    # ----------------------------

    def has_path_dfs(self, u, v):
        """
        Returns True if there is a path from u to v using DFS
        """
        seen = set()

        def dfs(node):
            if node == v:
                return True
            seen.add(node)
            for nb in self.graph[node]:
                if nb not in seen and dfs(nb):
                    return True
            return False

        return dfs(u)

    def has_path_bfs(self, u, v):
        """
        Returns True if there is a path from u to v using BFS
        """
        seen = {u}
        q = deque([u])
        while q:
            node = q.popleft()
            if node == v:
                return True
            for nb in self.graph[node]:
                if nb not in seen:
                    seen.add(nb)
                    q.append(nb)
        return False

# ----------------------------
# Example Usage
# ----------------------------

edges = [(0,1),(1,2),(0,3)]
g = Graph(edges)

print("BFS from 0:", g.bfs(0))  # [0, 1, 3, 2]
print("DFS from 0:", g.dfs(0))  # [0, 1, 2, 3] (order may vary)

print("Path exists 0→2 (DFS)?", g.has_path_dfs(0, 2))  # True
print("Path exists 3→2 (BFS)?", g.has_path_bfs(3, 2))  # False''',
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
    if n <= 1:
        return n
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
    return dp[amount] if dp[amount] != float('inf') else -1

# Longest Common Subsequence (LCS)
def longest_common_subsequence(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
    return dp[m][n]

# 0/1 Knapsack problem
def knapsack(weights, values, W):
    n = len(weights)
    dp = [[0]*(W+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for w in range(W+1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][W]

# Unique paths in a grid (m x n)
def unique_paths(m, n):
    dp = [[1]*n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]

# ----------------------------
# Example Usage
# ----------------------------

print("Fibonacci(10):", fib(10))  # 55

coins = [1, 2, 5]
amount = 11
print("Coin change for 11:", coin_change(coins, amount))  # 3 (5+5+1)

s1, s2 = "abcde", "ace"
print("LCS length:", longest_common_subsequence(s1, s2))  # 3

weights = [1, 3, 4]
values = [15, 20, 30]
W = 4
print("0/1 Knapsack max value:", knapsack(weights, values, W))  # 35

m, n = 3, 7
print("Unique paths in 3x7 grid:", unique_paths(m, n))  # 28''',
        "leetcode_examples": [
            {
                "id": "LC 509",
                "title": "Fibonacci Number",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Return the n-th Fibonacci number.",
                "approach": "Use memoization to store previously computed Fibonacci numbers to avoid redundant calculations.",
                "code": '''def fib(n: int) -> int:
    memo = {0:0, 1:1}

    def f(x):
        if x in memo:
            return memo[x]
        else:
            memo[x] = f(x-1) + f(x-2)
            return memo[x]
    
    return f(n)'''
            },

            {
                "id": "LC 70",
                "title": "Climbing Stairs",
                "difficulty": "Easy",
                "complexity": "O(n) time, O(n) space",
                "description": "Return the number of distinct ways to climb to the top of a staircase with n steps.",
                "approach": "Use memoization to store previously computed results to avoid redundant calculations.",
                "code": '''def climbStairs(n: int) -> int:
    memo = {1:1, 2:2}
    def f(n):
        if n in memo:
            return memo[n]
        else:
            memo[n] = f(n-2) + f(n-1)
            return memo[n]
    
    return f(n)'''
            },

            {
                "id": "LC 746",
                "title": "Min Cost Climbing Stairs",
                "difficulty": "Easy",
                "complexity": "O(2^n) time, O(n) space",
                "description": "Return the minimum cost to reach the top of the floor.",
                "approach": "Use memoization to store previously computed costs to avoid redundant calculations.",
                "code": '''def minCostClimbingStairs(cost: List[int]) -> int:
    # Recursive Solution
    n = len(cost)

    def min_cost(i):
        if i < 2:
            return 0

        return min(cost[i-2] + min_cost(i-2),
                    cost[i-1] + min_cost(i-1))

    return min_cost(n)'''
            },

            {
                "id": "LC 198",
                "title": "House Robber",
                "difficulty": "Medium",
                "complexity": "O(2^n) time, O(n) space",
                "description": "Return the maximum amount of money you can rob without alerting the police.",
                "approach": "Use memoization to store previously computed maximum amounts to avoid redundant calculations.",
                "code": '''def rob(nums: List[int]) -> int:
    n = len(nums)

    def helper(i):
        if i == 0:
            return nums[0]
        if i == 1:
            return max(nums[0], nums[1])
        
        return max(nums[i] + helper(i-2),
                    helper(i-1))
    
    return helper(n-1)'''
            },

            {
                "id": "LC 62",
                "title": "Unique Paths",
                "difficulty": "Medium",
                "complexity": "O(2^(m*n)) time, O(m*n) space",
                "description": "Return the number of unique paths from the top-left to the bottom-right of a grid.",
                "approach": "Use memoization to store previously computed results to avoid redundant calculations.",
                "code": '''def uniquePaths(m: int, n: int) -> int:
    def paths(i, j):
        if i == j == 0:
            return 1
        elif i < 0 or j < 0 or i == m or j == n:
            return 0
        else:
            return paths(i-1, j) + paths(i, j-1)
    
    return paths(m-1, n-1)'''
            },

            {
                "id": "LC 53",
                "title": " Maximum Subarray (Kadane's Algorithm)",
                "difficulty": "Medium",
                "complexity": "O(n) time, O(1) space",
                "description": "Find the contiguous subarray with the largest sum.",
                "approach": "Kadane's Algorithm: keep track of the maximum sum ending at each position.",
                "code": '''def maxSubArray(nums: List[int]) -> int:
    max_sum = float('-inf')
    curr_sum = 0
    
    for i in range(len(nums)):
        curr_sum += nums[i]
        max_sum = max(max_sum, curr_sum)

        if curr_sum < 0:
            curr_sum = 0
    
    return max_sum'''
            },

            {
                "id": "LC 55",
                "title": " Jump Game",
                "difficulty": "Medium",
                "complexity": "O(Max(nums) ^ n) time, O(n) space",
                "description": "Determine if you can reach the last index of the array.",
                "approach": "Use recursion with memoization to avoid redundant calculations.",
                "code": '''def canJump(nums: List[int]) -> bool:
    n = len(nums)
    
    def can_reach(i):
        if i == n-1:
            return True
        
        for jump in range(1, nums[i]+1):
            if can_reach(i+jump):
                return True
        
        return False
    
    return can_reach(0)'''
            },
            {
                "id": "LC 322",
                "title": "Coin Change",
                "difficulty": "Medium",
                "complexity": "O(amount * coins) time, O(amount) space",
                "description": "Return the minimum number of coins needed to make up the given amount.",
                "approach": "Use dynamic programming to build up the solution from smaller subproblems.",
                "code": '''def coinChange(coins: List[int], amount: int) -> int:
    if amount == 0:
        return 0
    elif amount < 0:
        return -1

    min_cnt = -1
    for coin in coins:
        cnt = self.coinChange(coins, amount - coin)
        if cnt >= 0:
            min_cnt = cnt + 1 if min_cnt < 0 else min(min_cnt, cnt + 1)
    return min_cnt'''
            },

            {
                "id": "LC 300",
                "title": "Longest Increasing Subsequence",
                "difficulty": "Medium",
                "complexity": "O(n^2) time, O(n) space",
                "description": "Return the length of the longest increasing subsequence.",
                "approach": "Use dynamic programming to build up the solution from smaller subproblems.",
                "code": '''def lengthOfLIS(nums: List[int]) -> int:
    n = len(nums)
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)'''
            },

            {
                "id": "LC 1143",
                "title": "Longest Common Subsequence",
                "difficulty": "Medium",
                "complexity": "O(m*n) time, O(m*n) space",
                "description": "Return the length of the longest common subsequence.",
                "approach": "Use dynamic programming to build up the solution from smaller subproblems.",
                "code": '''def longestCommonSubsequence(self, text1: str, text2: str) -> int:

    m, n = len(text1), len(text2)
    dp = [[0] * (n+1) for _ in range(m + 1)]

    for i in range(1, m+1):
        for j in range(1, n+1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]'''
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
