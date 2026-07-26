import random
import time

from google import genai
from google.genai import errors

from utils.config import GEMINI_API_KEY, GEMINI_MODEL


class LLMService:
    """
    Resilient Gemini LLM service.

    Features:
    - Primary model
    - Retry with exponential backoff
    - Automatic fallback models
    - Graceful API error handling
    """

    def __init__(self):

        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing from .env"
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        # Primary model from .env
        self.primary_model = GEMINI_MODEL

        # Add ONLY models confirmed by your
        # `client.models.list()` output.
        self.models = [
            self.primary_model,
            "gemini-3.1-flash-lite",
        ]

        # Remove duplicates
        self.models = list(
            dict.fromkeys(self.models)
        )

    def generate(
        self,
        prompt: str,
        retries_per_model: int = 3
    ) -> str:

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        last_error = None

        for model in self.models:

            print(
                f"\nTrying Gemini model: {model}"
            )

            for attempt in range(
                retries_per_model
            ):

                try:

                    response = (
                        self.client.models.generate_content(
                            model=model,
                            contents=prompt
                        )
                    )

                    text = getattr(
                        response,
                        "text",
                        None
                    )

                    if not text:
                        raise RuntimeError(
                            "Gemini returned an empty response."
                        )

                    print(
                        f"Response generated using: {model}"
                    )

                    return text.strip()

                except errors.ServerError as exc:

                    last_error = exc

                    if attempt < retries_per_model - 1:

                        delay = (
                            2 ** attempt
                            + random.uniform(0, 1)
                        )

                        print(
                            f"{model} temporarily unavailable. "
                            f"Retrying in {delay:.1f}s..."
                        )

                        time.sleep(delay)

                    else:

                        print(
                            f"{model} unavailable. "
                            "Switching model..."
                        )

                except errors.APIError as exc:

                    last_error = exc

                    print(
                        f"{model} API error: {exc}"
                    )

                    # Try next configured model
                    break

                except Exception as exc:

                    last_error = exc

                    print(
                        f"{model} failed: {exc}"
                    )

                    break

        raise RuntimeError(
            "All configured Gemini models failed. "
            f"Last error: {last_error}"
        )