from typing import Literal, Optional

from pydantic import BaseModel
from pydantic.v1 import root_validator


class SummarizeRequest(BaseModel):
    file_path: str
    model: str
    provider: Literal['ollama', 'openai']
    openai_api_key: Optional[str] = None

    @root_validator
    def require_openai_key(cls, values):
        provider = values.get("provider")
        key = values.get("openai_api_key")
        if provider == "openai" and not key:
            raise ValueError("openai_api_key is required when provider is 'openai'")
        return values
