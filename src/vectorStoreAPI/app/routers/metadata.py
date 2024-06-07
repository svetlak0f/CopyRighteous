from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body, Path, UploadFile, File
from .sync_ingestion import metadata_handler
from ..schemas.video import VideoMetadata

router = APIRouter()

@router.get("/")
def get_all_videos_metadata() -> list[VideoMetadata]:
    result = metadata_handler.get_all_videos_metadata()
    result = list(map(lambda x: VideoMetadata(**x), result))
    return result

@router.get("/{video_id}")
def get_video_metadata(video_id: str) -> VideoMetadata:
    result = metadata_handler.get_video_metadata(video_id)
    if result:
        return VideoMetadata(**result)
    raise HTTPException(404)
    