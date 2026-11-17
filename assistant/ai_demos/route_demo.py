"""Demo of campus routing with BFS vs A*."""
from assistant.features import campus_nav as nav


def run_demo():
    print("\n" + "=" * 60)
    print("  Campus route demo: BFS (fewest stops) vs A* (shortest distance)")
    print("=" * 60)
    print("  Roads:")
    for a, b in nav.EDGES:
        print(f"    {a.title().replace('Cs ', 'CS '):<14} <-> {b.title().replace('Cs ', 'CS '):<14} {nav.dist(a, b):6.1f} m")
    print()
    print("  " + nav.route_between("main gate", "hostel"))
    print("\n  BFS ignores distances; A* uses them plus a straight-line heuristic.")
    print("=" * 60 + "\n")
