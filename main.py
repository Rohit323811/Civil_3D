from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()
app.mount("/", StaticFiles(directory=".", html=True), name="static")

API_KEY = "msy_IBNNTMAjvre1nee3hoAdQTfNARAbIvDc8QQ0"

@app.post("/generate")
async def generate_model(request: Request):
    body = await request.json()
    prompt = body.get("prompt")
    if not prompt:
        return {"success": False, "error": "Prompt is required."}

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = httpx.post(
            "https://api.meshy.ai/v1/text-to-3d",
            headers=headers,
            json={"prompt": prompt}
        )
        data = response.json()
        return {"success": True, "model_url": data.get("result", "Not Found")}
    except Exception as e:
        return {"success": False, "error": str(e)}
