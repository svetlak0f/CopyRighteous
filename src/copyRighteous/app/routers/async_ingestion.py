from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body, Path, UploadFile, File, BackgroundTasks
import requests
import os
from uuid import UUID, uuid4
from typing import Annotated, Optional
import magic
from pathlib import Path

from ..internal.vectorizer.main import ResnetVectorizer
from ..internal.qdrant_handler import VectorHandler
from ..internal.processing_pipeline import ProcessingPipeline
from ..internal.metadata_handler import MetadataHandler

from .sync_ingestion import video_processor, metadata_handler

blob_directory = "./data/videos/"

router = APIRouter()

@router.post("/upload_and_index_video")
async def upload_video(background_tasks: BackgroundTasks, video: UploadFile = File(), search_while_ingestion: bool = False):
    """
    Асинхронный эндпоинт загрузки видео и индексации видео
    флаг ```search_while_ingestion``` отвечает за поиск внутри базы перед загрузкой видео.
    В случае нахождения плагиата, видео не загружается в базу
    """
    save_path = blob_directory + video.filename
    video_id = Path(save_path).stem
    search_result = metadata_handler.get_video_metadata(video_id)
    if search_result:
        raise HTTPException(409, "Video already exists in index, delete it before reingesting")
    
    with open(save_path, "wb") as f:
        f.write(await video.read())

    background_tasks.add_task(video_processor.process_video, 
                              save_path, 
                              video_id=video_id,
                              search_while_ingestion=search_while_ingestion)

    return {"message": f"Video saved and indexing process has been started. Video_id: {video_id}"}


@router.post("/match_video_without_saving")
def match_video(background_tasks: BackgroundTasks, video: UploadFile = File()):
    """
    Асинхронный эндпоинт для проверки видео на плагиат без его загрузки в базу
    """
    save_path = blob_directory + video.filename

    with open(save_path, "wb") as f:
        f.write(video.file.read())


    background_tasks.add_task(video_processor.run_video_matching_by_path, 
                              video_path=save_path)
    
    return "Matching job started"
