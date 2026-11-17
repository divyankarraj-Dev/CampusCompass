"""
Simulated weather report (no API key needed). For a given city and date the
values are deterministic, so asking twice gives the same answer.
"""
import random
import re
from datetime import date

CONDITIONS = ["Sunny", "Partly cloudy", "Overcast", "Light rain", "Hot and humid", "Clear skies", "Windy"]


def extract_city(text):
    cleaned = re.sub(r"\b(what|is|the|weather|forecast|temperature|in|for|at|of|today|now|like|please|tell|me)\b",
                     " ", text, flags=re.I)
    return " ".join(cleaned.replace("?", " ").split()).title()


def get_weather(text):
    city = extract_city(text)
    if not city:
        return "Which city? Try 'weather Ahmedabad'."
    rnd = random.Random(f"{city.lower()}-{date.today()}")
    return (f"Weather in {city} (simulated data)\n"
            f"   Temperature : {rnd.randint(16, 38)} C\n"
            f"   Condition   : {rnd.choice(CONDITIONS)}\n"
            f"   Humidity    : {rnd.randint(35, 90)} %\n"
            f"   Wind        : {rnd.randint(4, 30)} km/h")
