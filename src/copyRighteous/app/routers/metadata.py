from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body, Path, UploadFile, File
from .sync_ingestion import metadata_handler, video_db_handler
from ..schemas.video import VideoMetadata
import os

router = APIRouter()

blob_directory = "./data/videos/"

@router.get("/")
def get_all_videos_metadata() -> list[VideoMetadata]:
    """
    Получить информацию о всех загруженных либо загружающихся в индекс видео
    """
    result = metadata_handler.get_all_videos_metadata()
    result = list(map(lambda x: VideoMetadata(**x), result))
    return result


@router.get("/indexing")
def get_indexing_videos() -> list[VideoMetadata]:
    """
    Получить список индексирующихся видео в базе
    """
    result = metadata_handler.get_indexing_videos()
    result = list(map(lambda x: VideoMetadata(**x), result))
    return result


@router.get("/indexed")
def get_indexed_videos() -> list[VideoMetadata]:
    """
    Получить список индексированных видео
    """
    result = metadata_handler.get_indexed_videos()
    result = list(map(lambda x: VideoMetadata(**x), result))
    return result


@router.get("/{video_id}")
def get_video_metadata(video_id: str) -> VideoMetadata:
    """
    Ивлечь метаданные определенного видео
    """
    result = metadata_handler.get_video_metadata(video_id)
    if result:
        return VideoMetadata(**result)
    raise HTTPException(404)
    

@router.delete("/{video_id}")
def delete_video(video_id: str):
    """
    Полностью удалить видео из индекса
    """
    result = metadata_handler.get_video_metadata(video_id)
    if result:
        video_db_handler.delete_vectors_by_video_id(video_id)
        metadata_handler.delete_video_metadata(video_id)
        try:
            os.remove(os.path.join(blob_directory, f"{video_id}.mp4"))
        except:
            pass
        return "ok"
    raise HTTPException(404)
    