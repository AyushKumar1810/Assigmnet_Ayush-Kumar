# Girus Technical Coding Interview Solutions
# Author:`` AYUSH KUMAR (ayushsri1810@gmail.com)
# Language: Python 3
# Date: June 7, 2025

# ---------------------
# Problem 1: Sudoku Validator With Custom Zones
# ----------------------
def is_valid_sudoku(board, custom_zones):
    def is_valid_block(block):
        nums = [num for num in block if num != '.']
        return len(nums) == len(set(nums))

    for i in range(9):
        if not is_valid_block(board[i]) or not is_valid_block([board[j][i] for j in range(9)]):
            return False

    for x in range(0, 9, 3):
        for y in range(0, 9, 3):
            if not is_valid_block([board[i][j] for i in range(x, x+3) for j in range(y, y+3)]):
                return False

    for zone in custom_zones:
        if not is_valid_block([board[i][j] for (i, j) in zone]):
            return False

    return True

# Sample Test Case for Problem 1
sudoku_board = [
    ["5","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".","4","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"]
]
custom_zones = [
    [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)],
    [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)],
    # Define remaining 7 zones similarly...
]
print("Problem 1 Valid:", is_valid_sudoku(sudoku_board, custom_zones))

# ----------------------
# Problem 2: Alien Dictionary
# ----------------------
from collections import defaultdict, deque

def alien_order(words):
    graph = defaultdict(set)
    indegree = {c: 0 for word in words for c in word}

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in graph[c1]:
                    graph[c1].add(c2)
                    indegree[c2] += 1
                break
        else:
            if len(w1) > len(w2): return ""

    queue = deque([c for c in indegree if indegree[c] == 0])
    res = []
    while queue:
        c = queue.popleft()
        res.append(c)
        for nei in graph[c]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)
    return ''.join(res) if len(res) == len(indegree) else ""

# Sample Test Case for Problem 2
alien_words = ["wrt", "wrf", "er", "ett", "rftt"]
print("Problem 2 Order:", alien_order(alien_words))

# ----------------------
# Problem 3: Knights and Portals
# ----------------------
from collections import deque

def shortest_path_with_teleport(grid):
    n, m = len(grid), len(grid[0])
    visited = set()
    teleport_spots = [(i, j) for i in range(n) for j in range(m) if grid[i][j] == 0]
    queue = deque([(0, 0, False, 0)])  # x, y, used_teleport, dist

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    while queue:
        x, y, used, dist = queue.popleft()
        if (x, y, used) in visited:
            continue
        visited.add((x, y, used))

        if (x, y) == (n-1, m-1):
            return dist

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == 0:
                queue.append((nx, ny, used, dist+1))

        if not used:
            for tx, ty in teleport_spots:
                if (tx, ty) != (x, y):
                    queue.append((tx, ty, True, dist+1))

    return -1

# Sample Test Case for Problem 3
grid_map = [
    [0, 1, 1],
    [0, 0, 1],
    [1, 0, 0]
]
print("Problem 3 Path Length:", shortest_path_with_teleport(grid_map))

# ----------------------
# Problem 4: Bitwise Matching Pattern
# ----------------------
def next_higher_same_ones(n):
    c = n
    c0 = c1 = 0

    while ((c & 1) == 0) and (c != 0):
        c0 += 1
        c >>= 1

    while (c & 1) == 1:
        c1 += 1
        c >>= 1

    if c0 + c1 == 31 or c0 + c1 == 0:
        return -1

    p = c0 + c1
    n |= (1 << p)
    n &= ~((1 << p) - 1)
    n |= (1 << (c1 - 1)) - 1

    return n

# Sample Test Case for Problem 4
print("Problem 4 Next Number:", next_higher_same_ones(156))

# ----------------------
# Problem 5: Matrix Islands with Diagonals
# ----------------------
def num_islands_with_diagonals(grid):
    n, m = len(grid), len(grid[0])
    visited = [[False]*m for _ in range(n)]

    def dfs(i, j):
        if i < 0 or j < 0 or i >= n or j >= m or visited[i][j] or grid[i][j] == 0:
            return
        visited[i][j] = True
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            dfs(i + dx, j + dy)

    count = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1 and not visited[i][j]:
                dfs(i, j)
                count += 1
    return count

# Sample Test Case for Problem 5
matrix_islands = [
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]
print("Problem 5 Island Count:", num_islands_with_diagonals(matrix_islands))

# ----------------------
# Bonus Challenge: Mini Interpreter
# ----------------------
def evaluate_expression(s):
    env = {}
    def eval_tokens(tokens):
        stack = []
        i = 0
        while i < len(tokens):
            if tokens[i] == "let":
                var, val = tokens[i+1], int(tokens[i+2])
                env[var] = val
                i += 3
            elif tokens[i] == "if":
                cond = tokens[i+1]
                val = env.get(cond, 0)
                i += 2
                if val:
                    stack.append(tokens[i])
                else:
                    i += 2
            else:
                if tokens[i].isdigit():
                    stack.append(int(tokens[i]))
                elif tokens[i] in env:
                    stack.append(env[tokens[i]])
                i += 1
        return stack[-1] if stack else None

    return eval_tokens(s.replace('(', ' ').replace(')', ' ').split())

# Sample Test Case for Bonus Challenge
print("Bonus Interpreter Output:", evaluate_expression("let x 1 if x 10"))
