# Viva Preparation – Compass

**1. What is your project?**
A campus virtual assistant. It understands sentences using a Naive Bayes classifier and helps with routes, tasks,
maths, weather and Wikipedia; an AI Lab runs the syllabus algorithms.

**2. How does the assistant understand a sentence?**
It counts words per intent in training data, then picks the intent with the highest P(intent) × ΠP(word|intent).
Below 30 % confidence it says it did not understand.

**3. Why Naive Bayes? What is "naive" about it?**
It is simple, fast and works with little data. "Naive" means it assumes words are independent given the intent.

**4. Why smoothing?**
A word never seen in an intent would give probability 0 and wipe out the whole product. Smoothing (α = 0.1) gives unseen words a small non-zero probability.

**5. Why logarithms?**
Multiplying many small probabilities underflows; adding logs is stable and gives the same ranking.

**6. BFS vs DFS?**
BFS uses a queue and finds the path with the fewest edges but needs more memory. DFS uses a stack, needs little memory, but may return a longer path.

**7. What is Iterative Deepening Search?**
Repeated depth-limited DFS with an increasing limit: it returns the shallowest solution like BFS with the memory of DFS.

**8. How does A\* work? Why did it differ from BFS on the map?**
A\* expands the node with the smallest f = g + h (cost so far + heuristic). BFS ignores distances and minimises stops; A\* minimises distance, so the routes can differ.

**9. Is your heuristic admissible?**
Yes: straight-line distance never exceeds the road length, so it never over-estimates and A\* stays optimal. For the 8-puzzle, Manhattan distance is also admissible.

**10. What is a local maximum, and what is hill climbing's weakness?**
A peak that is higher than its neighbours but not the best overall. Hill climbing only moves uphill, so it gets stuck; the demo shows this for x·sin(x).

**11. How does simulated annealing escape it?**
It accepts a worse move with probability e^(Δ/T). At high temperature it explores freely; as T falls it settles, so it can leave a local peak and still converge.

**12. How is the 8-puzzle solved?**
A\* over board states; moves are the blank sliding up/down/left/right; h = sum of Manhattan distances of tiles. Solvability is checked by counting inversions (must be even).

**13. Towers of Hanoi complexity?**
Move n−1 disks away, move the largest, move n−1 back: T(n) = 2T(n−1) + 1 = 2ⁿ − 1 moves.

**14. Why not use `eval` in the calculator?**
`eval` can execute arbitrary code. Parsing with `ast` and whitelisting operators removes that risk.

**15. How does the web interface work?**
`main.py` starts a small local server (Python `http.server`). The page sends the message to `/api/chat`; the server calls the same `core.detect` and `core.respond` functions as the terminal version and returns JSON.

**16. What are the limitations?**
Simulated weather, small training set, sample campus map, English only. Future work: voice, HMM for context, larger dataset.

**17. How did you test it?**
19 automated tests (intents, calculator safety, BFS/A\*, puzzle solver, to-do, web API with all demos) plus a held-out accuracy check: 43 of 45 sentences correct (95.6 %).
