import uvicorn
from fastapi import FastAPI
from routers.summarize import RouterSummarize

app = FastAPI(
    title="LLM Text Summarizer",
    version="1.0",
)

app.include_router(RouterSummarize.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
