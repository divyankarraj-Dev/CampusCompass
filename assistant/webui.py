"""
Compass web interface.

A small local web server built only on the Python standard library. It serves one
HTML page (assistant/web/index.html) and a JSON API that calls the very same
functions as the terminal version (core.detect / core.respond, todo, campus_nav,
and the AI demos), so there is a single copy of the AI logic.

The server listens on 127.0.0.1 only, i.e. it is reachable from your own computer.
"""
import builtins
import contextlib
import io
import json
import os
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from assistant import core
from assistant.features import campus_nav, todo

WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
MAX_MESSAGE = 500
_demo_lock = threading.Lock()  # demos temporarily replace input()/stdout, so run one at a time

# Descriptions shown on the AI Lab cards (same order as core.get_demos()).
DEMO_INFO = [
    {"desc": "Compare three uninformed searches on one graph and see which path each returns.",
     "tag": "Search"},
    {"desc": "Climb a bumpy function and watch it get trapped on a local peak.",
     "tag": "Local search"},
    {"desc": "Escape local peaks by sometimes accepting worse moves while the temperature cools.",
     "tag": "Local search"},
    {"desc": "Solve a scrambled 8-puzzle optimally with A* and the Manhattan-distance heuristic.",
     "tag": "Problem solving"},
    {"desc": "Solve Towers of Hanoi by recursion and verify the 2^n - 1 minimum.",
     "tag": "Problem solving",
     "input": {"type": "number", "label": "Disks", "min": 1, "max": 5, "value": 3}},
    {"desc": "BFS (fewest stops) versus A* (shortest distance) on the campus road graph.",
     "tag": "Search"},
    {"desc": "See the probabilities Compass's Naive Bayes classifier assigns to each intent.",
     "tag": "Probabilistic AI",
     "input": {"type": "text", "label": "Type a sentence", "value": "how do i reach the library"}},
]


def list_demos():
    demos = []
    for i, (title, _module) in enumerate(core.get_demos()):
        info = DEMO_INFO[i] if i < len(DEMO_INFO) else {"desc": "", "tag": ""}
        demos.append({"id": i, "title": title, **info})
    return demos


def run_demo(index, value=""):
    """Run console demo number `index` and return everything it printed.
    input() calls inside the demo are answered from `value`, then with a blank line."""
    demos = core.get_demos()
    if not 0 <= index < len(demos):
        raise ValueError("unknown demo")
    _title, module = demos[index]
    answers = [str(value)] if str(value).strip() else []
    buffer = io.StringIO()
    with _demo_lock:
        real_input = builtins.input
        builtins.input = lambda prompt="": answers.pop(0) if answers else ""
        try:
            with contextlib.redirect_stdout(buffer):
                module.run_demo()
        except Exception as exc:  # report the problem to the page instead of crashing the server
            buffer.write(f"\nError while running the demo: {exc}\n")
        finally:
            builtins.input = real_input
    return buffer.getvalue()


def chat(message):
    intent, confidence = core.detect(message)
    result = {"intent": intent, "confidence": round(confidence, 3)}
    if intent == "demo":
        result["reply"] = "Opening the AI Lab - pick any algorithm and press Run."
        result["open"] = "lab"
        return result
    result["reply"] = core.respond(intent, message)
    if intent == "route":
        places = campus_nav.find_places(message)
        if len(places) == 1:
            places.insert(0, "main gate")
        if len(places) >= 2 and places[0] != places[1]:
            result["route"] = places[:2]
    return result


def campus_map():
    return {"places": {n: {"x": x, "y": y} for n, (x, y) in campus_nav.COORDS.items()},
            "edges": campus_nav.EDGES}


def find_route(start, goal):
    if start not in campus_nav.COORDS or goal not in campus_nav.COORDS:
        raise ValueError("unknown place")
    if start == goal:
        raise ValueError("choose two different places")
    astar_path, metres = campus_nav.astar(start, goal)
    return {"bfs": campus_nav.bfs(start, goal), "astar": astar_path, "metres": round(metres, 1)}


class Handler(BaseHTTPRequestHandler):
    server_version = "Compass"

    def log_message(self, fmt, *args):  # keep the terminal clean
        pass

    def _send(self, code, body, content_type):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        try:
            if url.path in ("/", "/index.html"):
                with open(os.path.join(WEB_DIR, "index.html"), "rb") as fh:
                    self._send(200, fh.read(), "text/html; charset=utf-8")
            elif url.path == "/api/todos":
                self._json({"tasks": todo.get_tasks()})
            elif url.path == "/api/map":
                self._json(campus_map())
            elif url.path == "/api/demos":
                self._json({"demos": list_demos()})
            elif url.path == "/api/route":
                self._json(find_route(query.get("start", [""])[0], query.get("goal", [""])[0]))
            else:
                self._json({"error": "not found"}, 404)
        except ValueError as exc:
            self._json({"error": str(exc)}, 400)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(length) or b"{}")
            if not isinstance(data, dict):
                raise ValueError("expected a JSON object")
            path = urlparse(self.path).path
            if path == "/api/chat":
                message = str(data.get("message", "")).strip()[:MAX_MESSAGE]
                if not message:
                    raise ValueError("empty message")
                self._json(chat(message))
            elif path == "/api/todos":
                action = data.get("action")
                if action == "add":
                    note = todo.add_item(str(data.get("text", "")))
                elif action == "remove":
                    note = todo.remove_task(str(int(data.get("index", 0)) + 1))
                else:
                    raise ValueError("unknown action")
                self._json({"tasks": todo.get_tasks(), "message": note})
            elif path == "/api/demo":
                self._json({"output": run_demo(int(data.get("id", -1)), data.get("value", ""))})
            else:
                self._json({"error": "not found"}, 404)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self._json({"error": str(exc)}, 400)


def make_server(port=8000):
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def launch(port=8000, open_browser=True):
    """Start the web UI (tries the next free port if `port` is busy)."""
    server = None
    for candidate in range(port, port + 20):
        try:
            server = make_server(candidate)
            break
        except OSError:
            continue
    if server is None:
        print("Could not find a free port. Try: python main.py --port 9000")
        return False
    url = f"http://127.0.0.1:{server.server_address[1]}"
    print(f"\n  Compass is running at {url}\n  Press Ctrl+C to stop.\n")
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Compass stopped. Goodbye!\n")
    finally:
        server.server_close()
    return True
