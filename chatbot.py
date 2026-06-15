"""
chatbot.py
----------
SentimentWellnessBot: the Topic 5 traditional WellnessBot extended to call a
cloud AI sentiment-analysis service (Azure AI Language), with a local fallback.

Pipeline for each message:
    1. Guard against empty / malformed input.
    2. Handle explicit commands (help, disclaimer, sentiment <text>).
    3. Rule-based intents (greetings, emergencies, etc.).
    4. TF-IDF retrieval over the FAQ corpus.
    5. Graceful fallback for out-of-scope input.

The AI service is layered on top: every substantive user message is scored for
sentiment, and the bot adds a short empathetic acknowledgment when the message
reads as negative or positive. A dedicated "sentiment <text>" command returns
the full confidence scores so the AI service's output is visible.
"""

import re
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from knowledge_base import INTENTS, FAQS, DISCLAIMER
from sentiment import get_analyzer


class SentimentWellnessBot:
    """Traditional WellnessBot + cloud sentiment analysis."""

    SIMILARITY_THRESHOLD = 0.20

    def __init__(self, analyzer=None, verbose=True):
        self.name = "WellnessBot"
        # The sentiment backend (Azure if configured, else local).
        self.analyzer = analyzer if analyzer is not None else get_analyzer(verbose)

        self._compiled_intents = [
            {
                "tag": i["tag"],
                "patterns": [re.compile(p, re.IGNORECASE) for p in i["patterns"]],
                "response": i["response"],
            }
            for i in INTENTS
        ]
        self._faq_questions = [q for q, _ in FAQS]
        self._faq_answers = [a for _, a in FAQS]
        self._vectorizer = TfidfVectorizer(
            preprocessor=self._normalize, stop_words="english"
        )
        self._faq_matrix = self._vectorizer.fit_transform(self._faq_questions)

    # ------------------------------------------------------------------ #
    @staticmethod
    def _normalize(text):
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        return re.sub(r"\s+", " ", text).strip()

    def capabilities(self):
        topics = [
            "sleep", "hydration", "nutrition / healthy eating", "exercise",
            "stress and anxiety", "healthy habits", "caffeine", "blood pressure",
            "common cold care",
        ]
        topic_lines = "\n".join(f"  - {t}" for t in topics)
        return (
            "Here's what I can help with:\n"
            f"{topic_lines}\n"
            "I also read the sentiment of your messages using a cloud AI "
            "service, so I can respond more supportively.\n"
            "Commands you can type:\n"
            "  - 'help' or 'capabilities'  -> show this list\n"
            "  - 'sentiment <text>'        -> show the AI sentiment scores for <text>\n"
            "  - 'disclaimer'              -> show my medical disclaimer\n"
            "  - 'bye' or 'quit'           -> end the conversation\n"
            "Just ask a question in plain English and I'll do my best!"
        )

    # ------------------------------------------------------------------ #
    def _empathy_prefix(self, result):
        """Short, sentiment-driven acknowledgment prepended to substantive replies."""
        if result.label == "negative":
            return "I'm sorry you're dealing with that. "
        if result.label == "positive":
            return "Love the positive energy! "
        if result.label == "mixed":
            return "Sounds like a mix of ups and downs. "
        return ""

    def respond(self, message):
        """Return the bot's reply to a single user message."""
        if message is None:
            return "I didn't catch that. Could you type a question?"
        cleaned = message.strip()
        if not cleaned:
            return "It looks like you didn't type anything. Ask me a wellness question, or type 'help'."
        if not re.search(r"[a-zA-Z]", cleaned):
            return (
                "Hmm, I couldn't find any words in that. Could you rephrase as "
                "a sentence? Type 'help' to see what I can answer."
            )

        normalized = self._normalize(cleaned)

        # Explicit "sentiment <text>" command -> show the AI service output.
        if normalized.startswith("sentiment"):
            target = cleaned[len("sentiment"):].strip(" :")
            if not target:
                return "Usage: sentiment <some text to analyze>"
            return "Sentiment analysis -> " + self.analyzer.analyze(target).summary()

        if normalized in {"help", "capabilities", "what can you do", "commands", "menu"}:
            return self.capabilities()
        if normalized in {"disclaimer", "are you a doctor", "is this medical advice"}:
            return DISCLAIMER

        # Rule-based intents take precedence (emergencies, greetings, etc.).
        for intent in self._compiled_intents:
            if any(pat.search(cleaned) for pat in intent["patterns"]):
                return intent["response"]

        # Substantive message: analyze sentiment, then answer via retrieval.
        sentiment = self.analyzer.analyze(cleaned)
        answer, score = self._retrieve(cleaned)
        if score >= self.SIMILARITY_THRESHOLD:
            return self._empathy_prefix(sentiment) + answer

        # Out-of-scope: still acknowledge sentiment, then guide the user.
        return (
            self._empathy_prefix(sentiment)
            + "I'm not sure I understood that. I focus on general wellness "
            "topics. Try rephrasing, or type 'help' to see what I can answer."
        )

    def _retrieve(self, message):
        query_vec = self._vectorizer.transform([message])
        sims = cosine_similarity(query_vec, self._faq_matrix)[0]
        best_idx = sims.argmax()
        return self._faq_answers[best_idx], float(sims[best_idx])
