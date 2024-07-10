from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from fastapi.responses import FileResponse
import os
import uuid
from app.utils.ai_model import process_video

router = APIRouter()

UPLOAD_DIR = "uploads"
MODEL_PATH = "app/models/best.onnx"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/process-video/")
async def process_video_endpoint(file: UploadFile = File(...)):
    try:
        input_video_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.mp4")
        output_video_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_out.mp4")

        with open(input_video_path, "wb") as buffer:
            buffer.write(await file.read())

        max_score = process_video(input_video_path, output_video_path, MODEL_PATH)

        download_link = f"/download-video/{os.path.basename(output_video_path)}"
        return {"download_link": download_link, "max_score": max_score}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download-video/{video_filename}")
async def download_video(video_filename: str):
    video_path = os.path.join(UPLOAD_DIR, video_filename)
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")
    return FileResponse(video_path, media_type="video/mp4", filename=video_filename)