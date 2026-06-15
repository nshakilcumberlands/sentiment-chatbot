"""
config.py
---------
Runtime configuration for the sentiment-aware WellnessBot.

Following the assignment walkthrough, sensitive values (the Azure key and
endpoint) are read from environment variables rather than hard-coded. This
keeps secrets out of source control and out of the GitHub repository.

Set them before running, for example (Windows):

    SET MicrosoftAIServiceEndpoint=https://<your-resource>.cognitiveservices.azure.com/
    SET MicrosoftAPIKey=<one-of-your-language-service-keys>

or on macOS/Linux:

    export MicrosoftAIServiceEndpoint="https://<your-resource>.cognitiveservices.azure.com/"
    export MicrosoftAPIKey="<one-of-your-language-service-keys>"

If neither variable is set, the bot automatically falls back to a local,
offline sentiment analyzer so it still runs end to end.
"""

import os


class DefaultConfig:
    """Holds configuration values, read from the environment at runtime."""

    # --- Added for the AI-as-a-service assignment -----------------------
    # Azure AI Language (formerly Cognitive Services) credentials.
    # Retrieved with os.environ.get so the values live outside the code.
    ENDPOINT_URI = os.environ.get("MicrosoftAIServiceEndpoint", "")
    API_KEY = os.environ.get("MicrosoftAPIKey", "")

    @classmethod
    def azure_configured(cls):
        """True only when both the endpoint and key are present."""
        return bool(cls.ENDPOINT_URI) and bool(cls.API_KEY)


# Debugging aid mentioned in the walkthrough — uncomment to confirm the
# environment variables are being read correctly on startup. Leave commented
# in normal use so the key is never printed.
# print("ENDPOINT_URI:", DefaultConfig.ENDPOINT_URI)
