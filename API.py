import requests
from fastapi import FastAPI, HTTPException
from PIL import Image, ImageFilter
from io import BytesIO
import Pixel_To_ASCII as pi

def endpoint():
    app = FastAPI()

    @app.post("/convert")
    async def convert_image(url: str, resolution: str = "low", blur: bool = False):
        try:
            # Download image from Unsplash
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))

            # Apply resolution and blur settings
            if resolution == "low":
                image = image.resize((100, 100))
            elif resolution == "high":
                image = image.resize((400, 400))
            if blur:
                image = image.filter(ImageFilter.GaussianBlur(5))

            # Convert image to ASCII
            ascii_art = pi.image_to_ascii(image)
            return {"ascii": ascii_art}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app

# run app with fastapi
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(endpoint(), host="0.0.0.0", port=8000)