"""
test_chatbot.py
---------------
Tests for the sentiment-aware WellnessBot. These run against the LOCAL
sentiment backend so they need no Azure credentials and no network.

Run with:
    python -m pytest -q
    python test_chatbot.py
"""

from chatbot import SentimentWellnessBot
from sentiment import LocalSentimentAnalyzer

# Force the offline analyzer so tests are deterministic and network-free.
bot = SentimentWellnessBot(analyzer=LocalSentimentAnalyzer(), verbose=False)


def test_greeting():
    assert "WellnessBot" in bot.respond("hi")


def test_capabilities_lists_sentiment():
    reply = bot.respond("help")
    assert "sentiment" in reply.lower()


def test_sentiment_command_negative():
    reply = bot.respond("sentiment I am exhausted and stressed")
    assert "negative" in reply.lower()


def test_sentiment_command_positive():
    reply = bot.respond("sentiment I feel great and happy")
    assert "positive" in reply.lower()


def test_empathy_prefix_on_negative_question():
    # Clearly negative wording (no positive tokens) should trigger empathy.
    reply = bot.respond("I am exhausted and stressed about my sleep")
    assert reply.lower().startswith("i'm sorry")


def test_faq_retrieval_still_works():
    reply = bot.respond("how much water should I drink daily")
    assert "cups" in reply.lower() or "hydrat" in reply.lower()


def test_malformed_symbols_only():
    reply = bot.respond("!!!###")
    assert "rephrase" in reply.lower() or "couldn't" in reply.lower()


def test_out_of_scope_fallback():
    reply = bot.respond("what is the capital of France?")
    assert "not sure" in reply.lower() or "wellness" in reply.lower()


def test_emergency_intent():
    reply = bot.respond("I think I'm having a heart attack")
    assert "emergency" in reply.lower() or "911" in reply


def _run_all():
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed.")


if __name__ == "__main__":
    _run_all()
