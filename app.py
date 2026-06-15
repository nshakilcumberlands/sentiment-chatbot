"""
app.py
------
Command-line front end for the sentiment-aware WellnessBot.

Run interactively:
    python app.py

Run a scripted demo (no user input required):
    python app.py --demo

On startup the program reports which sentiment backend is active (Azure when
the MicrosoftAIServiceEndpoint and MicrosoftAPIKey environment variables are
set, otherwise the local fallback).
"""

import sys

from chatbot import SentimentWellnessBot
from knowledge_base import DISCLAIMER

# Demo inputs chosen to exercise sentiment-aware replies plus every code path:
# positive, negative, neutral retrieval, the sentiment command, an emergency,
# malformed input, an out-of-scope question, and a goodbye.
DEMO_INPUTS = [
    "Hi there!",
    "help",
    "I feel exhausted and stressed, how can I sleep better?",
    "I'm feeling great today, any tips to build a healthy habit?",
    "how much water should I drink every day?",
    "sentiment I am so anxious and overwhelmed lately",
    "!!!###",
    "what is the capital of France?",
    "thanks so much, this is helpful",
    "bye",
]


def _banner(bot):
    return (
        "=" * 66 + "\n"
        "  WellnessBot + Azure AI Language (sentiment-aware) chatbot\n"
        + "=" * 66 + "\n"
        + DISCLAIMER + "\n"
        + "Type 'help' for capabilities, 'sentiment <text>' to test the AI "
        "service, or 'quit' to exit.\n"
    )


def run_demo():
    bot = SentimentWellnessBot()
    print(_banner(bot))
    for user_text in DEMO_INPUTS:
        print(f"You: {user_text}")
        print(f"{bot.name}: {bot.respond(user_text)}\n")


def run_interactive():
    bot = SentimentWellnessBot()
    print(_banner(bot))
    while True:
        try:
            user_text = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{bot.name}: Goodbye!")
            break
        if user_text.strip().lower() in {"quit", "exit", "bye", "goodbye"}:
            print(f"{bot.name}: {bot.respond(user_text)}")
            break
        print(f"{bot.name}: {bot.respond(user_text)}\n")


def main():
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_interactive()


if __name__ == "__main__":
    main()
