"""
Intent recognition with a Naive Bayes classifier written from scratch.

    P(intent | words)  is proportional to  P(intent) * product of P(word | intent)

Lidstone (add-alpha) smoothing handles unseen words and log-probabilities
avoid numerical underflow.
"""
import math
import re
from collections import Counter, defaultdict

ALPHA = 0.1          # smoothing constant
MIN_CONFIDENCE = 0.30

TRAINING_DATA = {
    "greet": ["hello", "hi", "hey there", "good morning", "good evening", "hello buddy", "namaste"],
    "bye": ["bye", "goodbye", "see you later", "exit", "quit", "good night", "i am leaving"],
    "help": ["help", "what can you do", "show commands", "your features", "how to use you"],
    "time": ["what is the time", "tell me the time", "current time", "what time is it", "time now"],
    "date": ["what is the date today", "today's date", "which day is it", "tell me the date", "what day is today"],
    "joke": ["tell me a joke", "make me laugh", "say something funny", "i want a joke", "joke please"],
    "tip": ["give me a study tip", "how to study better", "help me focus", "exam preparation advice",
            "i cannot concentrate", "study advice"],
    "route": ["how do i go from library to canteen", "route from main gate to cs department",
              "find path to hostel", "directions to the auditorium", "how to reach sports ground",
              "navigate from admin block to library", "shortest way to canteen"],
    "todo_add": ["add buy notebook to my list", "remind me to submit assignment",
                 "add task finish lab record", "new todo prepare for viva", "add study for exam"],
    "todo_show": ["show my tasks", "what is on my list", "list my todos", "show to do list", "my tasks"],
    "todo_done": ["remove task 1", "mark task done", "delete todo 2", "complete task 1", "remove 3"],
    "calc": ["calculate 5 plus 3", "what is 12 times 4", "compute 100 divided by 5", "solve this math",
             "calculate square root"],
    "wiki": ["wiki machine learning", "tell me about neural networks", "search wikipedia for python",
             "look up artificial intelligence", "who is alan turing", "what is photosynthesis"],
    "weather": ["weather in ahmedabad", "what is the weather today", "temperature in mumbai",
                "will it rain", "weather forecast"],
    "demo": ["show ai demo", "run demo", "demonstrate algorithms", "show me bfs", "simulated annealing demo",
             "solve 8 puzzle", "towers of hanoi", "hill climbing"],
}


def tokenize(text):
    return re.findall(r"[a-z']+", text.lower())


class NaiveBayesIntent:
    def __init__(self):
        self.word_counts = defaultdict(Counter)
        self.doc_counts = Counter()
        self.vocab = set()

    def train(self, data):
        for label, sentences in data.items():
            for sentence in sentences:
                words = tokenize(sentence)
                self.word_counts[label].update(words)
                self.doc_counts[label] += 1
                self.vocab.update(words)

    def probabilities(self, text):
        """Return {intent: probability}, or {} if no known word is present."""
        words = [w for w in tokenize(text) if w in self.vocab]
        if not words:
            return {}
        n_docs = sum(self.doc_counts.values())
        v = len(self.vocab)
        logs = {}
        for label in self.doc_counts:
            total = sum(self.word_counts[label].values())
            score = math.log(self.doc_counts[label] / n_docs)
            for w in words:
                score += math.log((self.word_counts[label][w] + ALPHA) / (total + ALPHA * v))
            logs[label] = score
        top = max(logs.values())
        exp = {k: math.exp(s - top) for k, s in logs.items()}
        z = sum(exp.values())
        return {k: e / z for k, e in exp.items()}

    def predict(self, text):
        probs = self.probabilities(text)
        if not probs:
            return "unknown", 0.0
        best = max(probs, key=probs.get)
        if probs[best] < MIN_CONFIDENCE:
            return "unknown", probs[best]
        return best, probs[best]


model = NaiveBayesIntent()
model.train(TRAINING_DATA)
