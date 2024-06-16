from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body, Path, UploadFile, File
from .sync_ingestion import job_metadata_handler
from ..schemas.video import VideoMetadata, MatchingJobData
from ..internal.seqfinder import convert_matching_job_to_sumbission
from fastapi.responses import StreamingResponse 
import pandas as pd

import os
from uuid import UUID

router = APIRouter()

@router.get("/")
def get_all_jobs() -> list[MatchingJobData]:
    """
    Получить список всех заданий мэтчинга
    """
    return job_metadata_handler.get_all_jobs()

@router.get("/submission_file")
def get_all_videos_sumbission_files():
    """
    Получить сабмишен файл для всех файлов
    """
    jobs = job_metadata_handler.get_all_jobs()
    jobs = list(map(lambda x: MatchingJobData(**x), jobs))
    jobs = list(filter(lambda x: x.status == "Done" and x.results, jobs))
    sumbmissions = list(map(convert_matching_job_to_sumbission, jobs))
    sumbmissions = pd.concat(sumbmissions, axis=0, ignore_index=True)
    return StreamingResponse(
        iter([sumbmissions.to_csv(index=False)]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=data.csv"}
)

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