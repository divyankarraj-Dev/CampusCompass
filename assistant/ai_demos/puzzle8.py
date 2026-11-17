"""8-puzzle solved with A* (heuristic = sum of Manhattan distances of tiles)."""
import heapq
import random

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVES = {"Up": -3, "Down": 3, "Left": -1, "Right": 1}


def manhattan(state):
    total = 0
    for pos, tile in enumerate(state):
        if tile:
            goal_pos = tile - 1
            total += abs(pos // 3 - goal_pos // 3) + abs(pos % 3 - goal_pos % 3)
    return total


def neighbours(state):
    blank = state.index(0)
    for name, delta in MOVES.items():
        new = blank + delta
        if name == "Left" and blank % 3 == 0:
            continue
        if name == "Right" and blank % 3 == 2:
            continue
        if not 0 <= new < 9:
            continue
        s = list(state)
        s[blank], s[new] = s[new], s[blank]
        yield name, tuple(s)


def solvable(state):
    tiles = [t for t in state if t]
    inversions = sum(a > b for i, a in enumerate(tiles) for b in tiles[i + 1:])
    return inversions % 2 == 0


def solve(start):
    """Return (list_of_moves, list_of_states, nodes_expanded) or None."""
    heap = [(manhattan(start), 0, start)]
    parent = {start: (None, None)}
    g_cost = {start: 0}
    expanded = 0
    while heap:
        _, g, state = heapq.heappop(heap)
        if g > g_cost[state]:
            continue
        expanded += 1
        if state == GOAL:
            moves, states = [], [state]
            while parent[state][0] is not None:
                prev, move = parent[state]
                moves.append(move)
                states.append(prev)
                state = prev
            return moves[::-1], states[::-1], expanded
        for move, nxt in neighbours(state):
            if g + 1 < g_cost.get(nxt, 10 ** 9):
                g_cost[nxt] = g + 1
                parent[nxt] = (state, move)
                heapq.heappush(heap, (g + 1 + manhattan(nxt), g + 1, nxt))
    return None


def scramble(n=20, seed=None):
    rnd = random.Random(seed)
    state = GOAL
    for _ in range(n):
        state = rnd.choice(list(neighbours(state)))[1]
    return state


def show_boards(states, per_row=5):
    for i in range(0, len(states), per_row):
        chunk = states[i:i + per_row]
        for r in range(3):
            print("    " + "     ".join(" ".join(str(t) if t else "_" for t in s[3 * r:3 * r + 3]) for s in chunk))
        print()


def run_demo():
    print("\n" + "=" * 60)
    print("  8-Puzzle demo (A* with Manhattan-distance heuristic)")
    print("=" * 60)
    start = scramble(22, seed=3)
    print(f"  Start: {start}   solvable: {solvable(start)}   h(start) = {manhattan(start)}")
    result = solve(start)
    moves, states, expanded = result
    print(f"  Solved in {len(moves)} moves, nodes expanded: {expanded}")
    print(f"  Moves of the blank: {', '.join(moves)}\n")
    show_boards(states)
    print("  A* with an admissible heuristic always returns an optimal (shortest) solution.")
    print("=" * 60 + "\n")
