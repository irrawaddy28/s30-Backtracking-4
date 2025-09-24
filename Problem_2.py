'''
1087 Brace Expansion
https://leetcode.com/problems/brace-expansion/description/

You are given a string s representing a list of words. Each letter in the word has one or more options.
    If there is one option, the letter is represented as is.
    If there is more than one option, then curly braces delimit the options. For example, "{a,b,c}" represents options ["a", "b", "c"].

For example, if s = "a{b,c}", the first character is always 'a', but the second character can be 'b' or 'c'. The original list is ["ab", "ac"].

Return all words that can be formed in this manner, sorted in lexicographical order.

Example 1:
Input: s = "{a,b}c{d,e}f"
Output: ["acdf","acef","bcdf","bcef"]

Example 2:
Input: s = "abcd"
Output: ["abcd"]

Constraints:
1 <= s.length <= 50
s consists of curly brackets '{}', commas ',', and lowercase English letters.
s is guaranteed to be a valid input.
There are no nested curly brackets.
All characters inside a pair of consecutive opening and ending curly brackets are different.

Solution
1. DFS w/ Backtracking:
We format the string into character groups stored in sublists. Each sublist is sorted individually.
eg.  {a,b}c{d,e}f -> [ [a,b], [c], [d,e], [f] ] (there are 4 char groups: [a,b], [c], [d,e], [f])

Then we use DFS w/ backtracking to build all possible strings by picking one character from each group. When we finish all groups, we add the built string to the final result list.
https://youtu.be/c7PW52OPg2M?t=3454
Time: O(k^n), or O(k^(N/k)), Space: O(n + k^n)
n is the number of groups, k is the max group size and N is the total length of the string (hence, n = N/k)


'''
def expand(s):
    def dfs(blocks, i, path):
        ''' dfs with backtracking '''
        if i >= len(blocks):
            result.append(path)
            return

        block = blocks[i]
        for j in range(len(block)):
            path += block[j] # action
            dfs(blocks, i+1, path) # recursion
            path = path[:-1] # backtrack

    if not s:
        return ""
    N = len(s)
    blocks = []
    result = []
    # pre-prcessing step: format the input string to a list a characters
    # eg.  {a,b}c{d,e}f -> [ [a,b], [c], [d,e], [f] ]
    i = 0
    while i < N:
        c = s[i]
        block = []
        if c == "{":
            i += 1
            while s[i] != '}':
                if s[i] != ',': block.append(s[i])
                i += 1
            i += 1
        else:
            while s[i] != '{':
                block.append(s[i])
                i += 1
                if i >= N: break
            block = ["".join(block)]
        blocks.append(sorted(block))

    # Run dfs with backtracking
    dfs(blocks, 0, "")
    return result

def run_expand():
    tests = [("{a,b}c{d,e}f", ['acdf', 'acef', 'bcdf', 'bcef']),
             ("abcd", ['abcd']),
    ]
    for test in tests:
        s, ans = test[0], test[1]
        result = expand(s)
        print(f"\ns = {s}")
        print(f"result = {result}")
        success = (ans == result)
        print(f"Pass: {success}")
        if not success:
            print(f"Failed")
            return

run_expand()