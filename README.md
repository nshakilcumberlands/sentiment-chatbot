# WellnessBot + Azure AI Language (Sentiment-Aware Chatbot)

This project connects a traditional (non-LLM) chatbot to a **cloud AI-as-a-service**
offering. It extends WellnessBot with **sentiment analysis** from **Azure AI
Language** (formerly Azure Cognitive Services, Text Analytics) so the bot can
read the emotional tone of each message and respond more supportively.

## Origin of the code

The traditional chatbot core (`chatbot.py`, `knowledge_base.py`, `app.py`,
`test_chatbot.py`) is **copied and adapted from the Topic 5 "Prototype Simple
Traditional Chatbot" project** (the WellnessBot rule-based + TF-IDF retrieval
bot). It is copied here, rather than referenced, because this assignment asks us
to take that bot as a starting point and layer a cloud AI service on top of it
without disturbing the original project. The new pieces added for this
assignment are:

- `sentiment.py` — Azure AI Language integration plus a local fallback analyzer.
- `config.py` — `DefaultConfig` reading the Azure key/endpoint from environment
  variables.
- Sentiment hooks inside `chatbot.py` (empathetic prefixes and a `sentiment`
  command).

## What the AI service adds

- Every substantive message is scored for sentiment. Negative messages get a
  brief empathetic acknowledgment, positive ones an encouraging note.
- A `sentiment <text>` command returns the raw confidence scores
  (positive / neutral / negative), making the AI service's output visible.
- The bot still does everything the traditional version did: responds to many
  prompts, lists capabilities (`help`), and handles malformed input.

## Backends

| Backend | When used | Requires |
|---------|-----------|----------|
| **Azure AI Language** | When `MicrosoftAIServiceEndpoint` and `MicrosoftAPIKey` are set and the SDK is installed | Free Azure account + Language resource |
| **Local fallback** | Automatically, when no Azure credentials are present | Nothing (runs offline) |

The bot prints which backend is active on startup, so it always runs—even
without an Azure key.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure Azure (optional but required for real cloud calls)

1. Create a free Azure account: https://azure.microsoft.com/en-us/free/students
2. In the Azure Portal, create an **Azure AI Language** resource (free F0 tier).
3. Open the resource's **Keys and Endpoint** page; copy the endpoint and a key.
4. Set them as environment variables:

   **macOS/Linux**
   ```bash
   export MicrosoftAIServiceEndpoint="https://<your-resource>.cognitiveservices.azure.com/"
   export MicrosoftAPIKey="<your-key>"
   ```

   **Windows (Command Prompt)**
   ```bat
   SET MicrosoftAIServiceEndpoint=https://<your-resource>.cognitiveservices.azure.com/
   SET MicrosoftAPIKey=<your-key>
   ```

   (You can also copy `.env.example` to `.env` and fill it in.)

## Run

```bash
python app.py            # interactive
python app.py --demo     # scripted demo conversation
```

Example:

```
You: sentiment I am so anxious and overwhelmed lately
WellnessBot: Sentiment analysis -> negative (pos=0.00, neu=0.00, neg=1.00) via local
```

## Test

```bash
python -m pytest -q       # if pytest is installed
python test_chatbot.py    # plain runner (9 tests, run against the local backend)
```

## Files

| File | Purpose |
|------|---------|
| `app.py` | CLI front end (interactive + `--demo`). |
| `chatbot.py` | `SentimentWellnessBot`: traditional core + sentiment hooks. |
| `sentiment.py` | Azure + local sentiment backends and the `get_analyzer` factory. |
| `config.py` | `DefaultConfig` reading Azure credentials from the environment. |
| `knowledge_base.py` | Intents, FAQ corpus, disclaimer (from Topic 5). |
| `test_chatbot.py` | Nine tests covering every behavior. |
| `.env.example` | Template for the Azure environment variables. |
| `requirements.txt` | `scikit-learn`, `azure-ai-textanalytics`. |

## Security note

API keys are read from environment variables and never committed. `.env` is
git-ignored. If a key is ever exposed, regenerate it from the Keys and Endpoint
page in the Azure Portal.

## AI disclosure

Anthropic's Claude was used to help scaffold this project's code and draft the
accompanying report. All code was reviewed and tested by the author. See the
report's "Disclosure of AI Use" section for details.

## License

MIT — see `LICENSE`.
