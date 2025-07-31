from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import json
import logging

from .image_analysis import analyze_image
from .text_gen import generate_headline_subheadline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Optimeleon Headline Generator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Optimeleon Headline Generator API", "version": "1.0.0"}

@app.post("/generate-headline")
async def generate_headline(
    image: UploadFile = File(...),
    marketing_insights: str = Form(...),
    original_headline: str = Form(...),
):
    try:
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        try:
            insights = json.loads(marketing_insights)
            original = json.loads(original_headline)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
        if not isinstance(insights, list):
            raise HTTPException(status_code=400, detail="marketing_insights must be an array")
        if not isinstance(original, dict) or "headline" not in original or "subheadline" not in original:
            raise HTTPException(status_code=400, detail="original_headline must contain 'headline' and 'subheadline' keys")
        image_bytes = await image.read()
        logger.info(f"Analyzing image: {image.filename}")
        image_description = analyze_image(image_bytes)
        logger.info("Generating headline and subheadline")
        result = generate_headline_subheadline(
            image_description=image_description,
            marketing_insights=insights,
            original_headline=original
        )
        logger.info("Successfully generated headline and subheadline")
        return JSONResponse(result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 