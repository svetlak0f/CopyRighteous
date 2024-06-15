from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body, Path, UploadFile, File
from .sync_ingestion import job_metadata_handler
from ..schemas.video import VideoMetadata, MatchingJobData
import os
from uuid import UUID

blob_path = "./data/videos"

router = APIRouter()

@router.get("/videos/{video_id}")
def get_video(video_id: str):
    # Read the MP4 video file
    path = os.path.join(blob_path, video_id)
    with open(path, "rb") as video_file:
        video_data = video_file.read()

    # Set the response headers
    headers = {
        "Content-Disposition": "attachment; filename=video.mp4",
        "Content-Type": "video/mp4",
    }

    # Return the video file as a response
    return Response(content=video_data, media_type="video/mp4", headers=headers)