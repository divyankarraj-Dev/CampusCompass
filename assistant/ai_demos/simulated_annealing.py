"""
Simulated annealing on the same function as the hill-climbing demo.

A worse move is accepted with probability exp(delta / T). A high temperature T
allows exploration; as T cools the search settles, so it can escape local peaks.
"""
import math
import random

from assistant.ai_demos.hill_climbing import HIGH, LOW, f


def anneal(start=0.5, t0=10.0, cooling=0.98, t_min=0.01, step=4.0, seed=None, verbose=True):
    rnd = random.Random(seed)
    x, cur = start, f(start)
    best_x, best_v = x, cur
    t, it = t0, 0
    if verbose:
        print(f"  {'iter':>5} {'temp':>7} {'x':>7} {'f(x)':>7}   best so far")
    while t > t_min:
        cand = min(HIGH, max(LOW, x + rnd.uniform(-step, step)))
        delta = f(cand) - cur
        if delta > 0 or rnd.random() < math.exp(delta / t):
            x, cur = cand, f(cand)
        if cur > best_v:
            best_x, best_v = x, cur
        if verbose and it % 40 == 0:
            print(f"  {it:>5} {t:>7.3f} {x:>7.2f} {cur:>7.2f}   {best_v:.2f} at x={best_x:.2f}")
        t *= cooling
        it += 1
    return best_x, best_v, it


def run_demo():
    print("\n" + "=" * 60)
    print("  Simulated Annealing demo   f(x) = x * sin(x),  0 <= x <= 10")
    print("  Start at x=0.5 (where plain hill climbing gets stuck at x=2.03)")
    print("=" * 60)
    x, v, iters = anneal(seed=42)
    print(f"\n  Result after {iters} iterations: x = {x:.3f}, f(x) = {v:.3f}")
    wins = sum(anneal(seed=s, verbose=False)[1] > 7 for s in range(20))
    print(f"  Reached the global peak in {wins}/20 independent runs.")
    print("=" * 60 + "\n")
