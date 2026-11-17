"""Two-sentence Wikipedia summary (needs internet + `pip install wikipedia`)."""
import re

_NOISE = r"\b(search|wikipedia|wiki|look\s+up|tell\s+me\s+about|what\s+is|who\s+is|find|for)\b"


def get_summary(text):
    topic = re.sub(_NOISE, "", text, flags=re.I).strip(" ?.,")
    if not topic:
        return "What topic? Try 'wiki machine learning'."
    try:
        import wikipedia
    except ImportError:
        return "The 'wikipedia' package is missing. Run: pip install wikipedia"
    try:
        return f"{topic.title()}: " + wikipedia.summary(topic, sentences=2)
    except wikipedia.exceptions.DisambiguationError as exc:
        return f"'{topic}' is ambiguous. Did you mean: {', '.join(exc.options[:5])}?"
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{topic}'."
    except Exception as exc:  # network errors etc.
        return f"Could not reach Wikipedia ({type(exc).__name__}). Check your internet connection."
