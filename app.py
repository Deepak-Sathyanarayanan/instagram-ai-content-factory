import os
from datetime import datetime
from typing import Optional, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from crew import InstagramContentFactory

app = FastAPI(
    title="Inst Content Factory API",
    description="FastAPI wrapper over the local Ollama-powered Instagram content factory",
    version="1.0.0",
)

DEFAULT_AUDIENCE = "AI engineers, ML engineers, data scientists, and technical founders"
DEFAULT_GOAL = "educate a technical audience and attract followers interested in AI/ML systems"
DEFAULT_TONE = "technical, sharp, concise, slightly bold"


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3)
    audience: Optional[str] = DEFAULT_AUDIENCE
    goal: Optional[str] = DEFAULT_GOAL
    tone: Optional[str] = DEFAULT_TONE
    save_to_disk: bool = True


class GenerateResponse(BaseModel):
    success: bool
    topic: str
    audience: str
    goal: str
    tone: str
    output_dir: Optional[str] = None
    outputs: Dict[str, str]


def slugify(value: str) -> str:
    value = value.strip().lower()
    safe = []
    for ch in value:
        if ch.isalnum():
            safe.append(ch)
        elif ch in {" ", "-", "_", "/"}:
            safe.append("_")
    slug = "".join(safe)
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug.strip("_") or "topic"


def save_output(topic: str, outputs: Dict[str, str]) -> str:
    slug = slugify(topic)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = os.path.join("outputs", f"{ts}_{slug}")
    os.makedirs(outdir, exist_ok=True)

    for name, content in outputs.items():
        path = os.path.join(outdir, f"{name}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    return outdir


@app.post("/generate", response_model=GenerateResponse)
def generate_content(payload: GenerateRequest) -> GenerateResponse:
    try:
        factory = InstagramContentFactory()

        outputs = factory.run(
            topic=payload.topic,
            audience=payload.audience or DEFAULT_AUDIENCE,
            goal=payload.goal or DEFAULT_GOAL,
            tone=payload.tone or DEFAULT_TONE,
        )

        output_dir = save_output(payload.topic, outputs) if payload.save_to_disk else None

        return GenerateResponse(
            success=True,
            topic=payload.topic,
            audience=payload.audience or DEFAULT_AUDIENCE,
            goal=payload.goal or DEFAULT_GOAL,
            tone=payload.tone or DEFAULT_TONE,
            output_dir=output_dir,
            outputs=outputs,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Generation failed: {exc}")
