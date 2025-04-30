from langchain_ollama import ChatOllama

from adapters.llm_adapter import LLmAdapter


class OllamaAdapter(LLmAdapter):

    def __init__(self, model:str):
        self.llm = ChatOllama(model=model)

    def summarize(self, text: str) -> str:
        prompt = f'Summarize this text: \n\n{text}\n\nTL;DR'
        response = self.llm.invoke(prompt)
        return response.content.strip()
