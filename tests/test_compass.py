"""Run with:  python -m unittest discover -s tests -v"""
import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from assistant import core, webui                                   # noqa: E402
from assistant.ai_demos import hill_climbing, puzzle8               # noqa: E402
from assistant.features import calculator, campus_nav, todo         # noqa: E402
from assistant.intent import model                                  # noqa: E402


class IntentTests(unittest.TestCase):
    def test_common_sentences(self):
        cases = {"hello": "greet", "what time is it": "time", "tell me a joke": "joke",
                 "how do i reach the hostel": "route", "remind me to submit assignment": "todo_add",
                 "give me a study tip": "tip"}
        for text, expected in cases.items():
            self.assertEqual(model.predict(text)[0], expected, text)

    def test_unknown_gibberish(self):
        self.assertEqual(model.predict("asdfgh qwerty")[0], "unknown")

    def test_probabilities_sum_to_one(self):
        self.assertAlmostEqual(sum(model.probabilities("what is the weather").values()), 1.0)

    def test_rule_overrides(self):
        self.assertEqual(core.detect("12*(3+4)")[0], "calc")
        self.assertEqual(core.detect("todo add buy pen")[0], "todo_add")
        self.assertEqual(core.detect("sqrt(16)")[0], "calc")


class CalculatorTests(unittest.TestCase):
    def test_values(self):
        self.assertEqual(calculator.calculate("calculate 12 times 4"), "12 * 4 = 48")
        self.assertIn("= 56", calculator.calculate("(3+4)*2^3"))
        self.assertIn("= 4", calculator.calculate("sqrt(16)"))

    def test_rejects_code(self):
        for bad in ("__import__('os').system('echo hi')", "open('x')", "2**99999"):
            self.assertIn("could not", calculator.calculate(bad).lower(), bad)

    def test_divide_by_zero(self):
        self.assertIn("zero", calculator.calculate("5/0"))


class SearchTests(unittest.TestCase):
    def test_bfs_fewest_stops(self):
        self.assertEqual(campus_nav.bfs("library", "canteen"), ["library", "canteen"])

    def test_astar_is_shortest(self):
        path, metres = campus_nav.astar("main gate", "hostel")
        self.assertEqual(path, ["main gate", "admin block", "library", "canteen", "hostel"])
        self.assertAlmostEqual(metres, 415.6, delta=1.0)

    def test_places_in_order(self):
        self.assertEqual(campus_nav.find_places("from library to canteen"), ["library", "canteen"])


class PuzzleTests(unittest.TestCase):
    def test_solves_optimally(self):
        start = (1, 2, 3, 4, 0, 6, 7, 5, 8)
        moves, states, _ = puzzle8.solve(start)
        self.assertEqual(len(moves), 2)
        self.assertEqual(states[-1], puzzle8.GOAL)

    def test_solvable_parity(self):
        self.assertFalse(puzzle8.solvable((1, 2, 3, 4, 5, 6, 8, 7, 0)))


class LocalSearchTests(unittest.TestCase):
    def test_hill_climb_gets_stuck(self):
        self.assertLess(hill_climbing.hill_climb(0.5)[1], 2.0)
        self.assertGreater(hill_climbing.hill_climb(5.0)[1], 7.0)


class TodoTests(unittest.TestCase):
    def setUp(self):
        self._orig = todo.DATA_FILE
        self._tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self._tmp.close()
        todo.DATA_FILE = self._tmp.name
        todo._save([])

    def tearDown(self):
        todo.DATA_FILE = self._orig
        os.unlink(self._tmp.name)

    def test_add_list_remove(self):
        todo.add_task("add buy notebook to my list")
        todo.add_item("Add exactly this")
        self.assertEqual(todo.get_tasks(), ["buy notebook", "Add exactly this"])
        todo.remove_task("todo remove 1")
        self.assertEqual(todo.get_tasks(), ["Add exactly this"])


class WebApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = webui.make_server(0)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def call(self, path, body=None):
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(self.base + path, data=data,
                                     headers={"Content-Type": "application/json"} if data else {})
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as err:
            return err.code, err.read()

    def test_page_served(self):
        status, body = self.call("/")
        self.assertEqual(status, 200)
        self.assertIn(b"Compass", body)

    def test_chat_and_route(self):
        status, body = self.call("/api/chat", {"message": "route from library to canteen"})
        reply = json.loads(body)
        self.assertEqual(status, 200)
        self.assertEqual(reply["intent"], "route")
        self.assertEqual(reply["route"], ["library", "canteen"])

    def test_empty_and_bad_input(self):
        self.assertEqual(self.call("/api/chat", {"message": "  "})[0], 400)
        self.assertEqual(self.call("/api/route?start=nowhere&goal=library")[0], 400)
        self.assertEqual(self.call("/api/demo", {"id": 99})[0], 400)
        self.assertEqual(self.call("/nope")[0], 404)

    def test_all_demos_run(self):
        demos = json.loads(self.call("/api/demos")[1])["demos"]
        self.assertEqual(len(demos), 7)
        for demo in demos:
            value = demo.get("input", {}).get("value", "")
            output = json.loads(self.call("/api/demo", {"id": demo["id"], "value": value})[1])["output"]
            self.assertGreater(len(output), 100, demo["title"])
            self.assertNotIn("Error while running", output, demo["title"])

    def test_path_traversal_blocked(self):
        status, body = self.call("/../../etc/passwd")
        self.assertIn(status, (400, 404))


if __name__ == "__main__":
    unittest.main()
