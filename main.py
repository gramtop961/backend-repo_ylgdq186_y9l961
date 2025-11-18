import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import numpy as np

app = FastAPI(title="ICT Trading Engine API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ICTSignal(BaseModel):
    direction: str
    entry: float
    stop: float
    target: float
    reasoning: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=ICTSignal)
async def analyze(
    htf: UploadFile = File(..., description="High timeframe chart image"),
    ltf: UploadFile = File(..., description="Lower timeframe chart image"),
    symbol: Optional[str] = Form(None),
):
    """Stub endpoint: accepts two images and returns a placeholder ICT signal.
    We'll wire full analysis after UI + health checks.
    """
    try:
        # Basic validation that files are images
        for f in (htf, ltf):
            if not f.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail=f"Invalid file type: {f.filename}")
        # Load to ensure decodability
        _ = Image.open(htf.file).convert("RGB")
        _ = Image.open(ltf.file).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse images: {str(e)}")

    # Placeholder ICT logic output
    return ICTSignal(
        direction="long",
        entry=1.2345,
        stop=1.2320,
        target=1.2400,
        reasoning=(
            "HTF bias bullish via BOS; LTF shows sweep -> MSS -> FVG. Entry at OTE discount; RR ~ 2.2."
        ),
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
