"""
Hill climbing on a bumpy 1-D function with two peaks:

        f(x) = x * sin(x)      for 0 <= x <= 10

  local peak  near x = 2.03  (f = 1.82)
  global peak near x = 7.98  (f = 7.92)

Plain hill climbing gets stuck on the local peak if it starts on the wrong side.
Random restarts fix this.
"""
import math
import random

LOW, HIGH = 0.0, 10.0


def f(x):
    return x * math.sin(x)


def hill_climb(start, step=0.05):
    """Steepest-ascent hill climbing. Returns (x, f(x), steps)."""
    x, steps = start, 0
    while True:
        best = x
        for candidate in (x - step, x + step):
            if LOW <= candidate <= HIGH and f(candidate) > f(best):
                best = candidate
        if best == x:
            return x, f(x), steps
        x, steps = best, steps + 1


def run_demo():
    print("\n" + "=" * 60)
    print("  Hill Climbing demo   f(x) = x * sin(x),  0 <= x <= 10")
    print("  Local peak ~ x=2.03 (1.82)   Global peak ~ x=7.98 (7.92)")
    print("=" * 60)
    print(f"  {'start':>6}  {'end x':>7}  {'f(x)':>7}  {'steps':>5}  result")
    for start in (0.5, 1.0, 5.0, 9.0):
        x, val, steps = hill_climb(start)
        kind = "GLOBAL peak" if val > 7 else "stuck on local peak"
        print(f"  {start:>6.1f}  {x:>7.2f}  {val:>7.2f}  {steps:>5}  {kind}")

    rnd = random.Random(7)
    best = max((hill_climb(rnd.uniform(LOW, HIGH)) for _ in range(10)), key=lambda r: r[1])
    print(f"\n  Random restart (10 tries): best x={best[0]:.2f}, f={best[1]:.2f}")
    print("  Lesson: hill climbing only moves uphill, so it can be trapped by local maxima.")
    print("=" * 60 + "\n")
