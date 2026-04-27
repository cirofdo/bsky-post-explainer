from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.agent import explain

app = FastAPI(title="Bluesky Post Explainer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExplainRequest(BaseModel):
    url: str


@app.post("/explain")
def explain_post(request: ExplainRequest):
    explanation = explain(request.url)
    return {"explanation": explanation}


@app.get("/health")
def health():
    return {"status": "ok"}
