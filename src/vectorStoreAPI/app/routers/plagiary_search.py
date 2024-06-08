from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body, Path, UploadFile, File
import requests
import os
from uuid import UUID, uuid4
from typing import Annotated, Optional
import magic
from pathlib import Path
from qdrant_client.models import PointStruct, Filter, Record, ScoredPoint

from ..schemas.video import MatchingData
from .sync_ingestion import video_db_handler, metadata_handler
from ..internal.seqfinder import process_matching_results


router = APIRouter()

@router.get("/search")
def search_plagiary(video_id: str) -> list[MatchingData]:
    search_result = metadata_handler.get_video_metadata(video_id)
    if search_result:
        vector_search_results = video_db_handler.search_nearest_by_video_id(video_id)
        matching_data = process_matching_results(vector_search_results)
        return matching_data
    raise HTTPException(404)
