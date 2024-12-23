import warnings
warnings.filterwarnings("ignore", message="Setting `pad_token_id` to `eos_token_id`")

import logging
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from transformers import LlavaProcessor, LlavaForConditionalGeneration
import torch
import numpy as np
from PIL import Image
import io

# ------------- Logging Setup -------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ------------- Model Initialization -------------
logger.info("Loading model and processor...")

model_id = "llava-hf/llava-interleave-qwen-0.5b-hf"
processor = LlavaProcessor.from_pretrained(model_id)
processor.patch_size = 14
processor.vision_feature_select_strategy = "mean"

device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Running on device: {device.upper()}")

model_dtype = torch.float16 if device == "cuda" else torch.float32
model = LlavaForConditionalGeneration.from_pretrained(model_id, torch_dtype=model_dtype)
model.to(device)

# ------------- FastAPI App -------------
app = FastAPI()

# ------------- CORS Middleware (allow all) -------------
# You can restrict to specific origins/ports if needed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------- Helper Functions -------------
def generate_caption(image: Image.Image, user_prompt: str) -> str:
    """
    Given a PIL Image and user prompt, generate caption text using the LLava model.
    """

    # Construct the prompt for the model
    toks = "<image>"
    prompt = f"<|im_start|>user{toks}\n{user_prompt}<|im_end|><|im_start|>assistant"

    # Prepare the inputs
    inputs = processor(
        text=prompt, 
        images=[image],
        return_tensors="pt"
    ).to(device, model_dtype)

    # Generate
    output = model.generate(
        **inputs,
        max_new_tokens=150,
        do_sample=False,
        pad_token_id=model.config.eos_token_id
    )
    # Decode
    raw_caption = processor.decode(output[0][2:], skip_special_tokens=True)

    # Optionally, remove the prompt from the raw caption
    # This part depends on your specific prompt usage logic
    # For demonstration, let's simply return raw_caption:
    return raw_caption

def wrap_text(text: str, width: int = 30) -> str:
    """
    Simple text wrapper that splits text into multiple lines.
    """
    lines = []
    words = text.split()
    line = ""
    for word in words:
        if len(line + word) <= width:
            line += (" " + word) if line else word
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return "\n".join(lines)


# ------------- API Routes -------------
@app.get("/")
def home():
    """
    Health check endpoint.
    """
    logger.info("Health check endpoint was called.")
    return {"message": "Caption API is running."}


@app.post("/generate-caption")
async def generate_caption_api(
    prompt: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Generate a caption given an image and a user prompt.
    """
    logger.info(f"Received caption generation request with prompt: {prompt}")

    # Read the uploaded file into memory
    image_bytes = await file.read()

    # Convert bytes to a PIL Image
    try:
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        logger.error("Error reading the image file.", exc_info=True)
        return {"error": "Invalid image file."}

    # Generate the caption
    caption_raw = generate_caption(pil_image, prompt)
    logger.info(f"Generated raw caption: {caption_raw}")

    # Optionally wrap the text to keep it more readable
    caption_wrapped = wrap_text(caption_raw, width=40)

    # Return the result
    logger.info(f"Returning wrapped caption: {caption_wrapped}")
    return {
        "prompt": prompt,
        "caption_raw": caption_raw,
        "caption_wrapped": caption_wrapped
    }


# ------------- Main Entry Point (for local debugging) -------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
