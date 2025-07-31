# Optimeleon AI Headline Generator

A production-ready, modular API that generates personalized headlines and subheadlines for e-commerce landing pages, based on advertisement images, marketing insights, and the original page structure.

## Features
- **Image Analysis:** Extracts visual themes and emotions from ad images using HuggingFace BLIP model.
- **Text Generation:** Uses OpenAI GPT-4 to generate headlines/subheadlines matching the original style and structure.
- **Personalization:** Leverages marketing insights for tailored messaging.
- **Modular:** Swap out image or text modules easily.
- **Production Ready:** Dockerized, FastAPI-based, easy to deploy.

## Project Structure
```
app/
  main.py           # FastAPI app
  image_analysis.py # Image-to-text module (BLIP)
  text_gen.py       # Headline/subheadline generation (GPT-4)
  utils.py          # Helper functions
requirements.txt
Dockerfile
README.md
```

## Setup

### 1. Clone the repo
```
git clone <repo-url>
cd optimeleon_project
```

### 2. Set up API Keys
You'll need an OpenAI API key for text generation:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 3. Install dependencies (locally)
```
pip install -r requirements.txt
```

### 4. Run the API (locally)
```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Build & Run with Docker
```bash
# Set environment variable for Docker
export OPENAI_API_KEY="your-openai-api-key-here"

# Build and run
docker build -t optimeleon-headline .
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY optimeleon-headline
```

## API Usage

### Endpoint
`POST /generate-headline`

#### Request (multipart/form-data)
- `image`: file (advertisement image)
- `marketing_insights`: JSON stringified array of strings
- `original_headline`: JSON stringified object with `headline` and `subheadline` (HTML)

#### Example cURL
```bash
curl -X POST "http://localhost:8000/generate-headline" \
  -F "image=@/path/to/ad.jpg" \
  -F 'marketing_insights=["Comfortable shoes", "Great for beginners", "Lightweight design"]' \
  -F 'original_headline={"headline": "<h1>First Marathon Journey Begins.</h1>", "subheadline": "<p>Start your adventure today!</p>"}'
```

#### Response
```json
{
  "headline": "<h1>Your Personalized Marathon Adventure Starts Now!</h1>",
  "subheadline": "<p>Join thousands of runners embracing their first marathon with comfort and confidence.</p>"
}
```

## API Documentation
Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Customization
- **Image Analysis:** Modify `analyze_image()` in `image_analysis.py` to use different models (e.g., Google Vision API, CLIP).
- **Text Generation:** Modify `generate_headline_subheadline()` in `text_gen.py` to use different LLMs (e.g., LLaMA, Claude).

## Technologies Used
- **FastAPI:** Web framework
- **HuggingFace Transformers:** BLIP model for image captioning
- **OpenAI GPT-4:** Text generation
- **Docker:** Containerization
- **Pillow:** Image processing

## Error Handling
The API includes comprehensive error handling:
- Invalid file types
- Malformed JSON
- Missing required fields
- Model/API failures (with fallbacks)

---

**Optimeleon AI Engineer Challenge Solution** # optimeleon_project
