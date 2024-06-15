from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body, Path, UploadFile, File
import requests
import os
from uuid import UUID, uuid4
from typing import Annotated, Optional
import magic
from pathlib import Path

from ..internal.vectorizer.main import ResnetVectorizer
from ..internal.vectorizer import ClipVectorizer
from ..internal.qdrant_handler import VectorHandler
from ..internal.processing_pipeline import ProcessingPipeline
from ..internal.metadata_handler import MetadataHandler, JobMetadataHandler
from ..schemas.video import MatchingData, SpecifiedMatching
from ..internal.yolo_vectorizer import YoloDetector
from ..internal.seqfinder import process_matching_results
from ..internal.sound_matcher import compare_audio_of_video_fragments
from qdrant_client.models import ScoredPoint
from datetime import datetime


blob_directory = "./data/videos/"

# video_vectorizer = ClipVectorizer(device="mps")
video_vectorizer = ResnetVectorizer(device="mps")
video_db_handler = VectorHandler()
metadata_handler = MetadataHandler()
job_metadata_handler = JobMetadataHandler()

yolo_vectorizer = YoloDetector(video_vectorizer=video_vectorizer,
                               device="mps")

video_processor = ProcessingPipeline(video_vectorizer=video_vectorizer, 
                                     video_db_handler=video_db_handler,
                                     metadata_handler=metadata_handler,
                                     job_metadata_handler=job_metadata_handler,
                                     yolo_vectorizer=yolo_vectorizer)




router = APIRouter()

@router.post("/upload_and_index_video")
def upload_video(video: UploadFile = File(), search_while_ingestion: bool = False):
    """
    Эндпоинт предназначен для синхронной загрузки видео, вовзращает 200 в случае успешной загрузки и индексации
    флаг ```search_while_ingestion``` отвечает за поиск внутри базы перед загрузкой видео.
    В случае нахождения плагиата, видео не загружается в базу
    """
    save_path = blob_directory + video.filename
    video_id = Path(save_path).stem

    search_result = metadata_handler.get_video_metadata(video_id)
    if search_result:
        raise HTTPException(409, "Video already exists in index, delete it before reingesting")

    with open(save_path, "wb") as f:
        f.write(video.file.read())

    # try:
    video_processor.process_video(save_path, 
                                    video_id=video_id, 
                                    search_while_ingestion=search_while_ingestion)
    # except ValueError:
    #     raise HTTPException(422, "Error while processing, check media format")
    # except RuntimeError as e:
    #     raise HTTPException(500, f"Error while vector store uploading, details {e}")
    # except TypeError:
    #     raise HTTPException(422, f"Plagiary found for: {video_id}")

    return {"message": "Video saved and indexed successfully"}

@router.post("/match_video_without_saving")
def match_video(video: UploadFile = File()) -> list[MatchingData]:
    """
    Синхронный эндпоинт для проверки видео на плагиат без его загрузки в базу
    """
    save_path = blob_directory + video.filename

    with open(save_path, "wb") as f:
        f.write(video.file.read())

    # try:

    job_id = uuid4()
    job_metadata_handler.submit_matching_job(job_id=job_id,
                                            video_id=Path(video.filename).stem)

    results = video_processor.sync_video_processing(video_path=save_path)
    results_yolo = video_processor.sync_process_with_yolo(video_path=save_path)

    results.extend(results_yolo)

    # for result in results:
    #     sound_similarity_score = compare_audio_of_video_fragments(save_path, 
    #                                     f"./data/videos/{result.match_video_id}.mp4",
    #                                     starttime1=result.match_start_frame // 10, endtime1=result.match_end_frame // 10,
    #                                     starttime2=result.query_start_frame // 10, endtime2=result.query_end_frame // 10)
        
    #     result.sound_similarity_score = sound_similarity_score


    data = {
        "status": "Done",
        "finished_at": datetime.now(),
        "results": list(map(lambda x: x.model_dump(), results))
    }


    job_metadata_handler.update_matching_job(job_id,
                                                new_values=data)   


    # except:
    #     raise HTTPException(422, "Wrong video format")

    return results


@router.post("/match_video_without_saving_yolo")
def match_video(video: UploadFile = File()) -> list[MatchingData]:
    """
    Получение предсказаний используя только модель поиска вставок поверх видео
    """
    save_path = blob_directory + video.filename

    with open(save_path, "wb") as f:
        f.write(video.file.read())

    # try:
    results = video_processor.sync_process_with_yolo(video_path=save_path)
    # except:
    #     raise HTTPException(422, "Wrong video format")
    # finally:
    #     os.remove(save_path)

    return results


@router.post("/match_video_without_saving_raw")
def raw_vectors(video: UploadFile = File()) -> list[ScoredPoint]:
    """
    Получить результаты векторного поиска без пост-процессинга для каждого кадра видео
    """
    save_path = blob_directory + video.filename

    with open(save_path, "wb") as f:
        f.write(video.file.read())

    try:
        results = video_processor.sync_video_processing_raw(video_path=save_path)
    except:
        raise HTTPException(422, "Wrong video format")
    finally:
        os.remove(save_path)

    return results