"""Shows the Naive Bayes intent classifier's probabilities for any sentence."""
from assistant.intent import model


def run_demo():
    print("\n" + "=" * 60)
    print("  Naive Bayes intent classifier - see how Compass decides")
    print("  P(intent | words) ~ P(intent) * product of P(word | intent)")
    print(f"  Trained on {sum(model.doc_counts.values())} sentences, "
          f"{len(model.doc_counts)} intents, {len(model.vocab)} words")
    print("=" * 60)
    while True:
        try:
            text = input("\n  Sentence (blank to exit): ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not text:
            break
        probs = model.probabilities(text)
        if not probs:
            print("  No known words in that sentence.")
            continue
        for intent, p in sorted(probs.items(), key=lambda kv: -kv[1])[:4]:
            print(f"    {intent:<10} {p * 100:5.1f}%  {'#' * int(p * 30)}")
    print("=" * 60 + "\n")
