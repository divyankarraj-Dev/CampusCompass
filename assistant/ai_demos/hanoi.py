"""Towers of Hanoi solved by recursion."""


def solve(n, src, aux, dst, moves):
    if n == 0:
        return
    solve(n - 1, src, dst, aux, moves)
    moves.append((n, src, dst))
    solve(n - 1, aux, src, dst, moves)


def run_demo():
    print("\n" + "=" * 60)
    print("  Towers of Hanoi demo (recursion)")
    print("=" * 60)
    try:
        n = int(input("  Number of disks (1-5) [3]: ").strip() or 3)
    except ValueError:
        n = 3
    n = max(1, min(n, 5))
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    moves = []
    solve(n, "A", "B", "C", moves)
    print(f"\n  Start: {pegs}")
    for i, (disk, a, b) in enumerate(moves, 1):
        pegs[b].append(pegs[a].pop())
        print(f"  Move {i:>2}: disk {disk} from {a} to {b}    {pegs}")
    print(f"\n  Total moves = {len(moves)}  (minimum possible is 2^{n} - 1 = {2 ** n - 1})")
    print("=" * 60 + "\n")
