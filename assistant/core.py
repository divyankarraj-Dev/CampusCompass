"""
Core of Compass: intent detection and the main chat loop.

Detection is hybrid:
  1. explicit commands ('todo add ...', 'wiki ...', arithmetic) are matched by rules;
  2. everything else goes to the Naive Bayes intent classifier.
"""
import re

from assistant import ui
from assistant.intent import model
from assistant.features import calculator, campus_nav, datetime_feat, jokes, todo, weather, wiki_search

HELP = """
  Compass commands (natural sentences also work)
  --------------------------------------------------
  time / date                  current time or date
  route from X to Y            campus route (BFS + A*), e.g. route from library to canteen
  todo add <task>              add a task        | todo list | todo remove <N>
  calculate <expr>             e.g. calculate 25 * 4 + 10   or just  12*(3+4)
  wiki <topic>                 Wikipedia summary (needs internet)
  weather <city>               simulated weather
  joke / tip                   a joke or a study tip
  demo                         AI algorithm demos (BFS, DFS, IDS, Hill Climbing,
                               Simulated Annealing, 8-Puzzle, Hanoi, Naive Bayes)
  help / exit
"""

ARITHMETIC = re.compile(r"^[\d\s+\-*/().%^]+$")


def detect(text):
    """Return (intent, confidence)."""
    low = text.lower().strip()
    if ARITHMETIC.match(low) and re.search(r"\d\s*[+\-*/%^]", low):
        return "calc", 1.0
    if re.search(r"\b(sqrt|sin|cos|tan|log|ln)\s*\(", low):
        return "calc", 1.0
    if re.match(r"todo\b", low):
        if re.match(r"todo\s+(list|show|view)", low) or low == "todo":
            return "todo_show", 1.0
        if re.match(r"todo\s+(remove|delete|done)", low):
            return "todo_done", 1.0
        return "todo_add", 1.0
    for prefix, intent in (("wiki", "wiki"), ("search", "wiki"), ("weather", "weather"),
                           ("calc", "calc"), ("route", "route"), ("demo", "demo")):
        if low.startswith(prefix):
            return intent, 1.0
    return model.predict(text)


def get_demos():
    """Return [(title, module)] for every AI demo (used by the CLI and the GUI)."""
    from assistant.ai_demos import (bayes_demo, hanoi, hill_climbing, puzzle8, route_demo,
                                    search_demos, simulated_annealing)
    return [("BFS / DFS / Iterative Deepening", search_demos), ("Hill Climbing", hill_climbing),
            ("Simulated Annealing", simulated_annealing), ("8-Puzzle (A*)", puzzle8),
            ("Towers of Hanoi", hanoi), ("Campus route: BFS vs A*", route_demo),
            ("Naive Bayes intent explainer", bayes_demo)]


def run_demos():
    menu = get_demos()
    print(ui.color("header", "\n  ===== AI DEMOS ====="))
    for i, (name, _) in enumerate(menu, 1):
        print(f"   {i}. {name}")
    print("   0. Back")
    choice = input(ui.color("prompt", "  Select: ")).strip()
    if choice.isdigit() and 1 <= int(choice) <= len(menu):
        menu[int(choice) - 1][1].run_demo()
    elif choice != "0":
        ui.say("Please pick a number from the menu.")


def respond(intent, text):
    """Return the reply text for an intent (None means 'handled separately')."""
    handlers = {
        "greet": lambda: "Hello! I am Compass. Type 'help' to see what I can do.",
        "bye": lambda: "Goodbye! All the best for your studies.",
        "time": datetime_feat.get_time,
        "date": datetime_feat.get_date,
        "joke": jokes.get_joke,
        "tip": jokes.get_tip,
        "route": lambda: campus_nav.get_route(text),
        "todo_add": lambda: todo.add_task(text),
        "todo_show": todo.list_tasks,
        "todo_done": lambda: todo.remove_task(text),
        "calc": lambda: calculator.calculate(text),
        "wiki": lambda: wiki_search.get_summary(text),
        "weather": lambda: weather.get_weather(text),
        "help": lambda: HELP,
    }
    handler = handlers.get(intent)
    return handler() if handler else "Sorry, I did not understand that. Type 'help' for options."


def run():
    while True:
        try:
            text = input(ui.color("prompt", "You> ")).strip()
        except (EOFError, KeyboardInterrupt):
            ui.say("Goodbye!")
            break
        if not text:
            continue
        intent, confidence = detect(text)
        if intent == "demo":
            run_demos()
            continue
        ui.say(respond(intent, text))
        if confidence < 1.0:
            print(ui.color("dim", f"              (intent: {intent}, confidence {confidence:.0%})"))
        if intent == "bye":
            break
