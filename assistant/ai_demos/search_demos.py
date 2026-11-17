"""
Uninformed search demos: BFS, DFS and Iterative Deepening Search (IDS).

Graph (undirected):
    S - A, B        A - C, D        B - D, E
    C - F           D - G           E - G
"""
from collections import deque

GRAPH = {"S": ["A", "B"], "A": ["S", "C", "D"], "B": ["S", "D", "E"], "C": ["A", "F"],
         "D": ["A", "B", "G"], "E": ["B", "G"], "F": ["C"], "G": ["D", "E"]}


def _arrow(path):
    return " -> ".join(path)


def bfs(start, goal):
    print("\n  BFS (FIFO queue) - explores level by level")
    queue, seen, order = deque([[start]]), {start}, []
    while queue:
        path = queue.popleft()
        node = path[-1]
        order.append(node)
        print(f"    expand {node}   queue={[p[-1] for p in queue]}")
        if node == goal:
            print(f"    order: {_arrow(order)}")
            return path
        for nb in GRAPH[node]:
            if nb not in seen:
                seen.add(nb)
                queue.append(path + [nb])
    return None


def dfs(start, goal):
    print("\n  DFS (LIFO stack) - goes deep before backtracking")
    stack, seen, order = [[start]], set(), []
    while stack:
        path = stack.pop()
        node = path[-1]
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        print(f"    expand {node}   stack={[p[-1] for p in stack]}")
        if node == goal:
            print(f"    order: {_arrow(order)}")
            return path
        for nb in reversed(GRAPH[node]):
            if nb not in seen:
                stack.append(path + [nb])
    return None


def _depth_limited(node, goal, limit, path, visited):
    visited.append(node)
    if node == goal:
        return path
    if limit == 0:
        return None
    for nb in GRAPH[node]:
        if nb not in path:
            found = _depth_limited(nb, goal, limit - 1, path + [nb], visited)
            if found:
                return found
    return None


def ids(start, goal, max_depth=8):
    print("\n  IDS - repeated depth-limited DFS with growing limit")
    for limit in range(max_depth + 1):
        visited = []
        result = _depth_limited(start, goal, limit, [start], visited)
        print(f"    depth limit {limit}: visited {_arrow(visited)}")
        if result:
            return result
    return None


def run_demo():
    start, goal = "S", "E"
    print("\n" + "=" * 60)
    print(f"  Uninformed search demo: find '{goal}' starting from '{start}'")
    print("=" * 60)
    for name, algo in (("BFS", bfs), ("DFS", dfs), ("IDS", ids)):
        path = algo(start, goal)
        print(f"  {name} path: {_arrow(path)}  ({len(path) - 1} steps)")
    print("\n  Note: BFS and IDS return the shortest path (fewest edges); DFS may not,")
    print("        but DFS uses far less memory. IDS combines both advantages.")
    print("=" * 60 + "\n")
