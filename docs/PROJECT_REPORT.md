# Compass – AI Campus Assistant: Project Report

**Course:** AIP203 – Artificial Intelligence Lab  |  **Mini Project:** Build a Virtual Assistant
**Student:** Divyankar Raj  |  **Roll No.:** 2025KUAD3040  |  **Submitted to:** Dr. Pooja Sharma

## 1. Abstract
Compass is a virtual assistant for college students. It understands plain-English requests with a Naive Bayes
intent classifier implemented from scratch, and answers them using modules for campus navigation, to-do
management, calculation, weather and Wikipedia. A web interface provides a chat window, an interactive campus
map and an "AI Lab" that executes the search and optimisation algorithms studied in the course. The project is
written in Python using only the standard library.

## 2. Objectives (mapped to course outcomes)
| Outcome | How the project meets it |
|---|---|
| CO1 – Implement search algorithms | BFS, DFS, Iterative Deepening, A\*, Hill Climbing and Simulated Annealing are implemented and demonstrated |
| CO2 – Solve AI problems | 8-puzzle (A\*), Towers of Hanoi (recursion), campus routing (graph search) |
| CO3 – Design a chatbot / virtual assistant | Intent recognition + dialogue handlers + web chat interface |

## 3. System Design
**Architecture.** `index.html` (front-end) → JSON API in `webui.py` → `core.detect()` / `core.respond()` →
feature modules and AI demos. The terminal mode calls the same core functions, so the AI logic exists once.

**Intent recognition (Naive Bayes).** Training data: 86 example sentences over 15 intents. For a sentence
with words w₁…wₙ the classifier maximises P(c)·ΠP(wᵢ|c). Log-probabilities avoid underflow; Lidstone smoothing
(α = 0.1) handles unseen words; confidence below 30 % is rejected. A small set of rules handles explicit
commands (`todo add`, `wiki`, arithmetic) before the classifier – a hybrid approach that keeps precise commands
exact while allowing free-form language elsewhere.

**Campus navigation.** Eight locations with (x, y) coordinates and nine roads form a weighted graph. BFS gives the
route with the fewest stops; A\* with the Euclidean heuristic gives the shortest distance. The heuristic is
admissible because road length equals straight-line distance, so A\* is optimal.

**Safe calculator.** Expressions are parsed with `ast` and only whitelisted operators and functions are evaluated;
large exponents are refused. This avoids the code-injection risk of `eval`.

**AI Lab demos.** Each demo is a plain Python module with `run_demo()`; the web server captures its printed output.

## 4. Implementation Summary
* Language: Python 3 (standard library only). Front-end: HTML, CSS and JavaScript in one file.
* About 1,500 lines of code in 23 source files, plus 19 automated unit and integration tests.
* Persistent data: `data/todos.json`.

## 5. Results and Testing
| Check | Result |
|---|---|
| Automated tests (`python -m unittest discover -s tests`) | 19 / 19 pass |
| Intent accuracy on 45 unseen, hand-written sentences (3 per intent) | 43 / 45 = **95.6 %** |
| Misclassified | "help me" → tip; "any tips for exam preparation" → todo_add |
| BFS vs A\* (Main Gate → Hostel) | BFS: 4 stops via CS Department; A\*: 4 stops, **415.9 m** via Canteen – different routes, A\* shorter |
| Hill climbing on x·sin(x) | Start 0.5 or 1.0 → stuck at local peak (f = 1.82); start 5 or 9 → global peak (f = 7.91) |
| Simulated annealing from x = 0.5 | Reaches the global peak in **18 / 20** seeded runs |
| 8-puzzle (A\*, Manhattan) | Scrambled start solved optimally in 10 moves, 33 nodes expanded |
| Towers of Hanoi | n disks solved in exactly 2ⁿ − 1 moves |

_Note:_ the accuracy figure comes from a small hand-made test set, so it indicates behaviour rather than
proving general performance.

## 6. Limitations
Weather data is simulated; the training corpus is small; the map is a sample campus; only English is supported.

## 7. Future Scope
Voice interface; Hidden Markov Model for dialogue context; Wumpus World demo; larger dataset with a proper
confusion-matrix evaluation; real campus map and live weather.

## 8. Conclusion
Compass shows how classical AI techniques – probabilistic classification and state-space search – can be combined
into a useful, understandable assistant. All major topics of the lab syllabus appear in working, tested code
behind an easy-to-use interface.

## 9. References
1. G. F. Luger, *Artificial Intelligence: Structures and Strategies for Complex Problem Solving*, 5th Ed., 2005.
2. M. Geldard et al., *Practical Artificial Intelligence with Swift*, O'Reilly Media.
3. S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th Ed.
