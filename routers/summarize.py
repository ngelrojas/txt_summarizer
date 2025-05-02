import os
from typing import Type

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from adapters.ollama_adapter import OllamaAdapter
from adapters.openai_adapter import OpenAIAdapter
from summarize.summarize_response import SummarizeResponse
from summarize.summarize_request import SummarizeRequest
from extract_files.extract_text_file_pdf import extract_text_from_pdf

from connections.cnx import Base, get_db
from models.summarize_model import Summarize

from models.summarize_settings import SummarizeSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RouterSummarize:
    router = APIRouter(prefix="/summarize", tags=["summarize"])

    @router.post("/", response_model=SummarizeResponse)
    async def create(req: SummarizeRequest, db:Session = Depends(get_db)):
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

        settings = db.query(SummarizeSettings).first()
        if not settings:
            raise HTTPException(404, "No settings found")

        if settings.provider.lower() == "ollama":
            adapter = OllamaAdapter(model=str(settings.model))
        else:
            if not req.openai_api_key:
                raise HTTPException(400, "No OpenAI API key provided")
            adapter = OpenAIAdapter(model=str(settings.model), api_key=str(settings.open_ai_key))

        summary = adapter.summarize(raw_text)
        return SummarizeResponse(summary=summary)
