"""Jokes and study tips."""
import random

JOKES = [
    "Why did the AI go to school? To improve its learning rate!",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I would tell you a UDP joke, but you might not get it.",
    "Why was the neural network bad at parties? It kept overfitting to one conversation.",
    "A heuristic walks into a bar... and guesses it is the right one.",
    "Why did the student bring a ladder to the AI lab? To reach the higher-order functions.",
]

TIPS = [
    "Use the Pomodoro method: 25 minutes of study, then a 5-minute break.",
    "Solve previous year questions; they show the exam pattern.",
    "Explain a topic aloud as if teaching a friend. Gaps show up quickly.",
    "Sleep well before exams. Memory consolidates during sleep.",
    "Write and run code yourself instead of only reading it. Labs are learned by doing.",
]


def get_joke():
    return random.choice(JOKES)


def get_tip():
    return random.choice(TIPS)
