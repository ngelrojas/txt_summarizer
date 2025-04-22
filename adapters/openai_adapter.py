import openai

from adapters.llm_adapter import LLmAdapter


class OpenAIAdapter(LLmAdapter):

    def __init__(self, model: str, api_key: str):
        openai.api_key = api_key
        self.model = model

    def summarize(self, text: str) -> str:
        messages = [
            {"role": "system" ,"content": "You are a helpful assitant that summarize text."},
            {"role": "user" ,"content": f"Summarize this text:\n\n{text}\n\nTL;DR"},
        ]
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=150,
            temperature=0.8,
        )
        return resp.choices[0].message.content.strip()
