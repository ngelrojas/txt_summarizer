from pydantic import BaseModel


class SummarizeRequest(BaseModel):
    model: str
    file_path: str
