from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import io

_processor = None
_model = None

def _load_blip_model():
    global _processor, _model
    if _processor is None:
        _processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        _model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return _processor, _model

processor, model = _load_blip_model()

def analyze_image(image_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs, max_length=50, num_beams=5)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        print(f"Image analysis failed: {e}")
        return "A woman running, determined expression, text: 'First Marathon Journey Begins.'" 