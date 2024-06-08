from fastapi import Depends, HTTPException, APIRouter, Path, BackgroundTasks
import requests
import os
from uuid import UUID, uuid4
from typing import Annotated, Optional
import magic
from pathlib import Path
from qdrant_client.models import PointStruct, Filter, Record, ScoredPoint

from ..schemas.video import MatchingData
from .sync_ingestion import metadata_handler, video_processor


router = APIRouter()

@router.get("/search")
def async_search_plagiary(video_id: str, background_tasks: BackgroundTasks):
    search_result = metadata_handler.get_video_metadata(video_id)
    if search_result:
        background_tasks.add_task(video_processor.run_video_matching, video_id)
        return "Matching job submited"
    raise HTTPException(404)
