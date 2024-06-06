from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body, Path, UploadFile, File
import requests
import os
from uuid import UUID, uuid4
from typing import Annotated, Optional
import os
import magic


router = APIRouter()

@router.post("/upload_video/")
async def upload_video(video: UploadFile = File(...)):
    # Specify the directory where you want to save the video
    save_directory = "./data/videos/"
    
    file_type = magic.from_buffer(await video.read(), mime=True)
    if file_type != 'video/mp4':
        return {"message": "Invalid video format. Only MP4 videos are allowed."}

    # Save the video file to disk
    with open(save_directory + video.filename, "wb") as f:
        f.write(await video.read())
    
    return {"message": "Video saved successfully"}