from abc import ABC, abstractmethod

class LLmAdapter(ABC):

    @abstractmethod
    def summarize(self, text: str) -> str:
        """return the TL:DR summary for the given text"""
        pass
