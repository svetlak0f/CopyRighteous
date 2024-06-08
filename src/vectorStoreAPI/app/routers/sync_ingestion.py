from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body, Path, UploadFile, File
import requests
import os
from uuid import UUID, uuid4
from typing import Annotated, Optional
import magic
from pathlib import Path

from ..internal.vectorizer.main import ResnetVectorizer
from ..internal.qdrant_handler import VectorHandler
from ..internal.processing_pipeline import ProcessingPipeline
from ..internal.metadata_handler import MetadataHandler, JobMetadataHandler

blob_directory = "./data/videos/"

video_vectorizer = ResnetVectorizer(device="mps")
video_db_handler = VectorHandler()
metadata_handler = MetadataHandler()
job_metadata_handler = JobMetadataHandler()

video_processor = ProcessingPipeline(video_vectorizer=video_vectorizer, 
                                     video_db_handler=video_db_handler,
                                     metadata_handler=metadata_handler,
                                     job_metadata_handler=job_metadata_handler)

router = APIRouter()

@router.post("/upload_and_index_video")
async def upload_video(video: UploadFile = File(...)):
    save_path = blob_directory + video.filename
    with open(save_path, "wb") as f:
        f.write(await video.read())

    try:
        video_processor.process_video(save_path, video_id=Path(save_path).stem)
    except ValueError:
        raise HTTPException(422, "Error while processing, check media format")
    except RuntimeError as e:
        raise HTTPException(500, f"Error while vector store uploading, details {e}")

    return {"message": "Video saved and indexed successfully"}