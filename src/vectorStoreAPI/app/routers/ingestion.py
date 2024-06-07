from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body, Path, UploadFile, File
import requests
import os
from uuid import UUID, uuid4
from typing import Annotated, Optional
import magic

from ..internal.vectorizer.main import ResnetVectorizer
from ..internal.qdrant_handler import VectorHandler


blob_directory = "./data/videos/"

video_vectorizer = ResnetVectorizer(device="mps")
video_db_handler = VectorHandler()

router = APIRouter()

@router.post("/upload_video")
async def upload_video(video: UploadFile = File(...)):
    # Specify the directory where you want to save the video

    # Save the video file to disk
    save_path = blob_directory + video.filename,
    with open(save_path, "wb") as f:
        f.write(await video.read())

    try:
        result = video_vectorizer.process_video(video_path=save_path)
    except:
        os.remove(save_path)
        raise HTTPException(422, "Error while processing, check media format")
    
    try:
        video_db_handler.save_vectors(result.tolist(), video_id=video.filename)
    except Exception as e:
        os.remove(save_path)
        raise HTTPException(500, f"Error while vector store uploading, details {e}")


    return {"message": "Video saved successfully"}