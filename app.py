import uvicorn
from fastapi import FastAPI
from routers.summarize import RouterSummarize
from routers.summarize_settings import router as settings_router  # your file-settings endpoints

app = FastAPI(
    title="LLM Text Summarizer",
    version="1.0",
)

# Mount the summarization endpoints
app.include_router(RouterSummarize.router)

# Mount the file-settings endpoints
app.include_router(settings_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
