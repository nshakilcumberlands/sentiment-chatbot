"""
sentiment.py
------------
Sentiment analysis for the WellnessBot, with two interchangeable backends:

1. AzureSentimentAnalyzer - calls the Azure AI Language (Text Analytics)
   sentiment endpoint via the official azure-ai-textanalytics SDK. This is the
   cloud "AI-as-a-service" integration the assignment requires.

2. LocalSentimentAnalyzer - a small, dependency-free lexicon analyzer used as a
   fallback so the bot still runs when Azure credentials are not configured
   (for example, on a grader's machine without a key).

Both expose the same method, analyze(text) -> SentimentResult, so the rest of
the bot does not care which one is active. The get_analyzer() factory chooses
Azure when credentials are present and the SDK is installed, otherwise local.
"""

from dataclasses import dataclass

from config import DefaultConfig


@dataclass
class SentimentResult:
    """Normalized sentiment result shared by both backends."""
    label: str                     # "positive", "neutral", "negative", or "mixed"
    positive: float                # confidence scores in [0, 1]
    neutral: float
    negative: float
    backend: str                   # "azure" or "local"

    def summary(self):
        return (
            f"{self.label} "
            f"(pos={self.positive:.2f}, neu={self.neutral:.2f}, "
            f"neg={self.negative:.2f}) via {self.backend}"
        )


class AzureSentimentAnalyzer:
    """Wraps the Azure AI Language sentiment endpoint."""

    def __init__(self, endpoint, key):
        # Imported lazily so the package is only required when actually used.
        from azure.core.credentials import AzureKeyCredential
        from azure.ai.textanalytics import TextAnalyticsClient

        self._client = TextAnalyticsClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

    def analyze(self, text):
        # The API accepts a list of documents and returns a list of results.
        result = self._client.analyze_sentiment([text])[0]
        if result.is_error:
            raise RuntimeError(f"Azure error: {result.error}")
        s = result.confidence_scores
        return SentimentResult(
            label=result.sentiment,
            positive=s.positive,
            neutral=s.neutral,
            negative=s.negative,
            backend="azure",
        )


class LocalSentimentAnalyzer:
    """A tiny lexicon-based fallback analyzer (no network, no dependencies)."""

    POSITIVE = {
        "good", "great", "better", "love", "happy", "glad", "excited",
        "wonderful", "awesome", "calm", "relaxed", "hopeful", "improving",
        "strong", "energized", "rested", "thanks", "thank", "amazing",
    }
    NEGATIVE = {
        "bad", "worse", "worst", "tired", "exhausted", "sad", "stressed",
        "anxious", "anxiety", "depressed", "pain", "sick", "awful", "terrible",
        "struggling", "overwhelmed", "can't", "cannot", "hate", "worried",
        "hurts", "lonely", "burned", "burnout",
    }

    def analyze(self, text):
        words = "".join(c.lower() if c.isalpha() else " " for c in text).split()
        pos = sum(w in self.POSITIVE for w in words)
        neg = sum(w in self.NEGATIVE for w in words)
        total = pos + neg
        if total == 0:
            return SentimentResult("neutral", 0.0, 1.0, 0.0, "local")
        p, n = pos / total, neg / total
        if pos and neg:
            label = "mixed"
        elif pos:
            label = "positive"
        else:
            label = "negative"
        return SentimentResult(
            label=label,
            positive=round(p, 2),
            neutral=round(1 - abs(p - n), 2),
            negative=round(n, 2),
            backend="local",
        )


def get_analyzer(verbose=True):
    """
    Return an analyzer instance. Prefer Azure when configured and importable;
    otherwise fall back to the local analyzer. Never raises on missing Azure.
    """
    if DefaultConfig.azure_configured():
        try:
            analyzer = AzureSentimentAnalyzer(
                DefaultConfig.ENDPOINT_URI, DefaultConfig.API_KEY
            )
            if verbose:
                print("[sentiment] Using Azure AI Language service.")
            return analyzer
        except Exception as exc:  # SDK missing or bad credentials
            if verbose:
                print(f"[sentiment] Azure unavailable ({exc}); using local fallback.")
    elif verbose:
        print("[sentiment] No Azure credentials found; using local fallback.")
    return LocalSentimentAnalyzer()
