import os
from fastapi import APIRouter, HTTPException
from langchain_ollama import ChatOllama
from summarize.summarize_response import SummarizeResponse
from summarize.summarize_request import SummarizeRequest
from extract_files.extract_text_file_pdf import extract_text_from_pdf


class RouterSummarize:
    router = APIRouter(prefix="/summarize", tags=["summarize"])
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @router.post("/", response_model=SummarizeResponse)
    async def create(req: SummarizeRequest):
        rel = req.file_path.lstrip("./")
        model = req.model
        abs_path = os.path.join(RouterSummarize.BASE_DIR, rel)
        if not os.path.isfile(abs_path):
            raise HTTPException(404, f"File not found: {abs_path}")
        ext = os.path.splitext(abs_path)[1].lower()
        if ext == ".pdf":
            raw_text = extract_text_from_pdf(abs_path)
        else:
            with open(abs_path, encoding="utf-8") as f:
                raw_text = f.read()
        if not raw_text.strip():
            raise HTTPException(400, "No text extracted from file")

        llm = ChatOllama(model=model)
        prompt = f"Summarize this text:\n\n{raw_text}\n\nTL;DR:"
        response = llm.invoke(prompt)
        return SummarizeResponse(summary=response.content.strip())

    @router.get("/{summary_id}", response_model=SummarizeResponse)
    async def read(summary_id: str):
        pass

    @router.put("/{summary_id}", response_model=SummarizeResponse)
    async def update(summary_id: str, req: SummarizeRequest):
        pass

    @router.delete("/{summary_id}")
    async def delete(summary_id: str):
        pass
