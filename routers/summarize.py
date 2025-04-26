import os
from fastapi import APIRouter, HTTPException
from adapters.ollama_adapter import OllamaAdapter
from adapters.openai_adapter import OpenAIAdapter
from summarize.summarize_response import SummarizeResponse
from summarize.summarize_request import SummarizeRequest
from extract_files.extract_text_file_pdf import extract_text_from_pdf

from connections.cnx import SessionDep
from models.summarize_model import Summarize


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RouterSummarize:
    router = APIRouter(prefix="/summarize", tags=["summarize"])

    @router.post("/", response_model=SummarizeResponse)
    async def create(req: SummarizeRequest):
        rel = req.file_path.lstrip("./")
        abs_path = os.path.join(BASE_DIR, rel)
        if not os.path.isfile(abs_path):
            raise HTTPException(404, f"File not found: {abs_path}")

        ext = os.path.splitext(abs_path)[1].lower()
        if ext == ".pdf":
            raw_text = extract_text_from_pdf(abs_path)
        else:
            raw_text = open(abs_path, encoding="utf-8").read()

        if not raw_text.strip():
            raise HTTPException(400, "No text extracted from file")

        if req.provider == "ollama":
            adapter = OllamaAdapter(model=req.model)
        else:
            if not req.openai_api_key:
                raise HTTPException(400, "No OpenAI API key provided")
            adapter = OpenAIAdapter(model=req.model, api_key=req.openai_api_key)

        summary = adapter.summarize(raw_text)
        return SummarizeResponse(summary=summary)

    @router.get("/{summarize_id}")
    async def read(summarize_id: str, session: SessionDep) -> Summarize:
        try:
            summarize_txt = session.get(Summarize, summarize_id)
            if not summarize_txt:
                raise HTTPException(status_code=404, detail="Summarize not found")
            return summarize_txt
        except Exception as err:
            raise HTTPException(404, f"{err} No summary found with id: {summarize_id}")

    @router.put("/{summary_id}", response_model=SummarizeResponse)
    async def update(summary_id: str, req: SummarizeRequest):
        pass

    @router.delete("/{summary_id}")
    async def delete(summary_id: str):
        pass
