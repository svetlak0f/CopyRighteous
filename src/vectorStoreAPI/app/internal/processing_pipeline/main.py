from ..qdrant_handler import VectorHandler
from ..vectorizer import ResnetVectorizer, AbstractVideoVectorizer
from ...internal.yolo_vectorizer import YoloDetector
from ..metadata_handler import MetadataHandler, JobMetadataHandler
import os
from pathlib import Path
from datetime import datetime

from uuid import uuid4
from ..seqfinder import process_matching_results
from ...schemas.video import MatchingData

class ProcessingPipeline:

    def __init__(self, 
                 video_vectorizer: AbstractVideoVectorizer, 
                 video_db_handler: VectorHandler,
                 metadata_handler: MetadataHandler,
                 job_metadata_handler: JobMetadataHandler,
                 yolo_vectorizer: YoloDetector):
        
        self.video_vectorizer = video_vectorizer
        self.video_db_handler = video_db_handler
        self.metadata_handler = metadata_handler
        self.job_metadata_handler = job_metadata_handler
        self.yolo_vectorizer = yolo_vectorizer

    def process_video(self, video_path, video_id, search_while_ingestion: bool = False):
        # try:
        self.metadata_handler.add_new_video_metadata(video_id)
        result, frames_count, video_time, framerate = self.video_vectorizer.process_video(video_path=video_path)
        metadata = {
            "frames_count": frames_count,
            "video_time": str(video_time),
            "framerate": framerate
        }
        self.metadata_handler.update_video_metadata(video_id=video_id, new_values=metadata)
        # except:
        #     os.remove(video_path)
        #     metadata = {
        #         "status": "Error",
        #     }
        #     self.metadata_handler.update_video_metadata(video_id=video_id, new_values=metadata)
        #     raise ValueError("Error while processing, check media format")
        
        if search_while_ingestion:
            job_id = uuid4()
            self.job_metadata_handler.submit_matching_job(job_id=job_id,
                                            video_id=video_id)
            
            matched_vectors = self.video_db_handler.query_vectors_batch(result.tolist())

            matching_data = process_matching_results(matched_vectors)

            data = {
                "status": "Done",
                "finished_at": datetime.now(),
                "results": list(map(lambda x: x.model_dump(), matching_data))
            }

            self.job_metadata_handler.update_matching_job(job_id,
                                                        new_values=data)   
            
            if matching_data:
                os.remove(video_path)
                metadata = {
                    "status": "Plagiary found",
                }
                self.metadata_handler.update_video_metadata(video_id=video_id, new_values=metadata)
                raise TypeError("Finded plagiary")

        try:
            self.video_db_handler.save_vectors(result.tolist(), video_id=video_id)
            metadata = {
                "status": "Indexed",
                "indexed_at": datetime.now()
            }
            self.metadata_handler.update_video_metadata(video_id=video_id, new_values=metadata)
        except:
            os.remove(video_path)
            metadata = {
                "status": "Error",
            }
            self.metadata_handler.update_video_metadata(video_id=video_id, new_values=metadata)
            raise RuntimeError("Error while ingestion into database")
        

    def sync_video_processing(self, video_path: str) -> list[MatchingData]:
        result, frames_count, video_time, framerate = self.video_vectorizer.process_video(video_path=video_path)
        matched_vectors = self.video_db_handler.query_vectors_batch(result.tolist())
        matching_data = process_matching_results(matched_vectors, max_skip=10, min_length=70)
        return matching_data


    def sync_process_with_yolo(self, video_path: str):
        yolo_matches = self.yolo_vectorizer.process_video_frames(video_path=video_path)
        matching_data = list()
        for yolo_match in yolo_matches:
            results = self.video_db_handler.query_vectors_batch(yolo_match.vectors)
            matching = process_matching_results(results=results, max_skip=10, min_length=70, input_offset=yolo_match.start)
            matching_data.extend(matching)
        
        return matching_data

    def run_video_matching(self, video_id):
        job_id = uuid4()
        # try:
        self.job_metadata_handler.submit_matching_job(job_id=job_id,
                                                    video_id=video_id)
        vector_search_results = self.video_db_handler.search_nearest_by_video_id(video_id)
        matching_data = process_matching_results(vector_search_results)

        data = {
            "status": "Done",
            "finished_at": datetime.now(),
            "results": list(map(lambda x: x.model_dump(), matching_data))
        }

        self.job_metadata_handler.update_matching_job(job_id,
                                                    new_values=data)
        # except:
        #                 data = {
        #         "status": "Done",
        #         "finished_at": datetime.now(),
        #         "results": list(map(lambda x: x.model_dump(), matching_data))
        #     }

        #     self.job_metadata_handler.update_matching_job(job_id,
        #                                                 new_values=data)
        

