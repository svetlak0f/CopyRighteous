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
from qdrant_client.models import ScoredPoint


blob_directory = "./data/videos/"

video_vectorizer = ClipVectorizer(device="mps")
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
def match_video(video: UploadFile = File()) -> SpecifiedMatching:
    save_path = blob_directory + video.filename

    with open(save_path, "wb") as f:
        f.write(video.file.read())

    # try:
    results = video_processor.sync_video_processing(video_path=save_path)
    results_yolo = video_processor.sync_process_with_yolo(video_path=save_path)
    # except:
    #     raise HTTPException(422, "Wrong video format")
    # finally:
    #     os.remove(save_path)

    response = SpecifiedMatching(classical_search=results,
                                 yolo_matching=results_yolo)

    return response


@router.post("/match_video_without_saving_yolo")
def match_video(video: UploadFile = File()) -> list[MatchingData]:
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