"""
knowledge_base.py
-----------------
Knowledge base for the sentiment-aware WellnessBot.

Carried over (with minor additions) from the Topic 5 "Prototype Simple
Traditional Chatbot" project. It holds:

1. INTENTS  - rule/pattern-based intents matched with regular expressions.
2. FAQS     - a retrieval corpus of health/wellness question-answer pairs used
              with TF-IDF + cosine similarity.

The traditional (non-LLM) matching is unchanged; this project layers a cloud
AI sentiment-analysis service on top of it.
"""

DISCLAIMER = (
    "I'm an informational wellness bot, not a medical professional. "
    "For diagnosis, treatment, or emergencies, please contact a qualified "
    "healthcare provider or your local emergency number."
)

INTENTS = [
    {
        "tag": "greeting",
        "patterns": [
            r"\b(hi|hello|hey|good morning|good afternoon|good evening|greetings)\b",
        ],
        "response": (
            "Hello! I'm WellnessBot, your general health and wellness "
            "assistant. Ask me about sleep, hydration, nutrition, exercise, "
            "stress, and more. Type 'help' to see what I can do."
        ),
    },
    {
        "tag": "goodbye",
        "patterns": [r"\b(bye|goodbye|see you|farewell|exit|quit)\b"],
        "response": "Take care of yourself! Remember to rest, hydrate, and move. Goodbye!",
    },
    {
        "tag": "thanks",
        "patterns": [r"\b(thanks|thank you|appreciate it|thx)\b"],
        "response": "You're very welcome! Is there anything else I can help you with?",
    },
    {
        "tag": "identity",
        "patterns": [r"\b(who are you|what are you|your name)\b"],
        "response": (
            "I'm WellnessBot, a rule-based and retrieval-based chatbot that now "
            "also reads the sentiment of your messages using a cloud AI service "
            "so I can respond more empathetically."
        ),
    },
    {
        "tag": "emergency",
        "patterns": [
            r"\b(chest pain|can'?t breathe|suicid|kill myself|overdose|"
            r"heart attack|stroke|bleeding badly|unconscious)\b",
        ],
        "response": (
            "This may be a medical emergency. Please call your local emergency "
            "number (911 in the U.S.) or go to the nearest emergency room right "
            "now. If you are in the U.S. and in crisis, you can also call or "
            "text 988 for the Suicide and Crisis Lifeline."
        ),
    },
]

FAQS = [
    (
        "How much water should I drink each day?",
        "A common guideline is about 8 cups (roughly 2 liters) of fluids a "
        "day, but needs vary with body size, activity, and climate. A simple "
        "check: pale-yellow urine usually means you're well hydrated.",
    ),
    (
        "How many hours of sleep do adults need?",
        "Most adults need 7 to 9 hours of sleep per night. Keeping a regular "
        "sleep schedule and limiting screens before bed can improve sleep quality.",
    ),
    (
        "How can I improve my sleep quality?",
        "Try a consistent bedtime, a cool and dark room, limiting caffeine "
        "after early afternoon, and avoiding screens for 30-60 minutes before bed.",
    ),
    (
        "How much exercise should I get per week?",
        "Adults are generally advised to get at least 150 minutes of moderate "
        "aerobic activity per week, plus muscle-strengthening activities on two "
        "or more days.",
    ),
    (
        "What is a balanced diet?",
        "A balanced diet emphasizes vegetables, fruits, whole grains, lean "
        "proteins, and healthy fats, while limiting added sugar, sodium, and "
        "highly processed foods.",
    ),
    (
        "How can I reduce stress?",
        "Helpful strategies include regular physical activity, deep-breathing "
        "or mindfulness, adequate sleep, social connection, and breaking large "
        "tasks into smaller steps. Persistent stress is worth discussing with a "
        "professional.",
    ),
    (
        "How can I manage anxiety?",
        "Grounding techniques, paced breathing, regular exercise, limiting "
        "caffeine, and consistent sleep can help. If anxiety interferes with "
        "daily life, consider speaking with a licensed mental-health provider.",
    ),
    (
        "What are some healthy snacks?",
        "Good options include fruit, vegetables with hummus, plain yogurt, "
        "nuts, or whole-grain crackers. These provide nutrients without a lot "
        "of added sugar.",
    ),
    (
        "How can I lower my blood pressure naturally?",
        "Lifestyle steps that may help include reducing sodium, staying "
        "active, maintaining a healthy weight, limiting alcohol, and managing "
        "stress. Always coordinate changes with your doctor.",
    ),
    (
        "How do I start a running routine?",
        "Begin with a walk-run approach: alternate one minute of jogging with "
        "one to two minutes of walking, and build gradually. Good shoes and "
        "rest days help prevent injury.",
    ),
    (
        "What should I do for a common cold?",
        "Rest, fluids, and time are the mainstays. Over-the-counter remedies "
        "may ease symptoms. See a provider if you have a high fever, trouble "
        "breathing, or symptoms that worsen after several days.",
    ),
    (
        "How can I build a healthy habit?",
        "Start small, attach the new habit to an existing routine, track your "
        "progress, and be patient — consistency matters more than intensity "
        "at the beginning.",
    ),
    (
        "Why is hydration important?",
        "Water supports temperature regulation, joint lubrication, nutrient "
        "transport, and waste removal. Even mild dehydration can affect energy "
        "and concentration.",
    ),
    (
        "How much caffeine is safe per day?",
        "For most healthy adults, up to about 400 mg of caffeine a day "
        "(roughly four cups of coffee) is considered moderate. Sensitivity "
        "varies, so adjust to how you feel.",
    ),
]
