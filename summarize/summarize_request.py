from pydantic import BaseModel


class SummarizeRequest(BaseModel):
    file_path: str
