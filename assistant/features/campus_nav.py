"""
Campus route finder on a weighted graph of campus locations.
  * BFS  -> path with the fewest stops          (uninformed search)
  * A*   -> path with the shortest distance     (informed search, Euclidean heuristic)
"""
import heapq
import math
from collections import defaultdict, deque

COORDS = {  # (x, y) in metres on an imaginary campus map
    "main gate": (0, 0), "admin block": (100, 40), "library": (180, 90),
    "cs department": (260, 40), "canteen": (200, 180), "auditorium": (120, 160),
    "hostel": (320, 200), "sports ground": (80, 260),
}
EDGES = [("main gate", "admin block"), ("admin block", "library"), ("admin block", "auditorium"),
         ("library", "cs department"), ("library", "canteen"), ("auditorium", "canteen"),
         ("auditorium", "sports ground"), ("canteen", "hostel"), ("cs department", "hostel")]
ALIASES = {"cs": "cs department", "gate": "main gate", "admin": "admin block", "sports": "sports ground",
           "ground": "sports ground", "mess": "canteen"}


def dist(a, b):
    (x1, y1), (x2, y2) = COORDS[a], COORDS[b]
    return math.hypot(x1 - x2, y1 - y2)


GRAPH = defaultdict(list)
for _u, _v in EDGES:
    GRAPH[_u].append((_v, dist(_u, _v)))
    GRAPH[_v].append((_u, dist(_u, _v)))


def bfs(start, goal):
    queue, seen = deque([[start]]), {start}
    while queue:
        path = queue.popleft()
        if path[-1] == goal:
            return path
        for nxt, _ in GRAPH[path[-1]]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(path + [nxt])
    return None


def astar(start, goal):
    heap = [(dist(start, goal), 0.0, start, [start])]
    best = {start: 0.0}
    while heap:
        _, g, node, path = heapq.heappop(heap)
        if node == goal:
            return path, g
        for nxt, w in GRAPH[node]:
            if g + w < best.get(nxt, float("inf")):
                best[nxt] = g + w
                heapq.heappush(heap, (g + w + dist(nxt, goal), g + w, nxt, path + [nxt]))
    return None, 0.0


def find_places(text):
    """Known places mentioned in the text, in order of appearance."""
    text = text.lower()
    hits = []
    for name in list(COORDS) + list(ALIASES):
        pos = text.find(name)
        if pos != -1:
            hits.append((pos, ALIASES.get(name, name)))
    ordered = []
    for _, place in sorted(hits):
        if place not in ordered:
            ordered.append(place)
    return ordered


def route_between(start, goal):
    show = lambda p: " -> ".join(x.title().replace("Cs ", "CS ") for x in p)
    a_path, metres = astar(start, goal)
    return (f"Fewest stops (BFS) : {show(bfs(start, goal))}\n"
            f"   Shortest walk (A*) : {show(a_path)}  (~{metres:.0f} m)")


def get_route(text):
    places = find_places(text)
    if len(places) == 1:
        places.insert(0, "main gate")  # default starting point
    if len(places) < 2 or places[0] == places[1]:
        return ("Tell me two places, e.g. 'route from library to canteen'.\n   Known places: "
                + ", ".join(p.title() for p in COORDS))
    return route_between(places[0], places[1])
