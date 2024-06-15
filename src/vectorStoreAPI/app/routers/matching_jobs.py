from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body, Path, UploadFile, File
from .sync_ingestion import job_metadata_handler
from ..schemas.video import VideoMetadata, MatchingJobData
import os
from uuid import UUID

router = APIRouter()

@router.get("/")
def get_all_jobs() -> list[MatchingJobData]:
    """
    Получить список всех заданий мэтчинга
    """
    return job_metadata_handler.get_all_jobs()

@router.get("/active")
def get_all_active_jobs() -> list[MatchingJobData]:
    """
    Получить только активные задания мэтчинга
    """
    return job_metadata_handler.get_active_jobs()
    

@router.get("/by_video/{video_id}")
def get_all_jobs_by_video_id(video_id: str) -> list[MatchingJobData]: 
    """
    Получить все работы по идентификатору видео
    """
    result = job_metadata_handler.get_job_metadata_by_video_id(video_id)
    if result:
        result = list(map(lambda x: MatchingJobData(**x), result))
        return result
    raise HTTPException(404)


@router.get("/{job_id}")
def get_specific(job_id: UUID) -> MatchingJobData:
    """
    Получить конкретное задание по идентификатору
    """
    result = job_metadata_handler.get_job_metadata(job_id)
    if result:
        return result
    raise HTTPException(404)