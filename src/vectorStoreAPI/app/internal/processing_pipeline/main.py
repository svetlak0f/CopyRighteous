from ..qdrant_handler import VectorHandler
from ..vectorizer import ResnetVectorizer, AbstractVideoVectorizer
from ..metadata_handler import MetadataHandler, JobMetadataHandler
import os
from pathlib import Path
from datetime import datetime

from uuid import uuid4
from ..seqfinder import process_matching_results


class ProcessingPipeline:

    def __init__(self, 
                 video_vectorizer: AbstractVideoVectorizer, 
                 video_db_handler: VectorHandler,
                 metadata_handler: MetadataHandler,
                 job_metadata_handler: JobMetadataHandler):
        
        self.video_vectorizer = video_vectorizer
        self.video_db_handler = video_db_handler
        self.metadata_handler = metadata_handler
        self.job_metadata_handler = job_metadata_handler

    def process_video(self, video_path, video_id):
        try:
            self.metadata_handler.add_new_video_metadata(video_id)
            result, frames_count, video_time, framerate = self.video_vectorizer.process_video(video_path=video_path)
            metadata = {
                "frames_count": frames_count,
                "video_time": str(video_time),
                "framerate": framerate
            }
            self.metadata_handler.update_video_metadata(video_id=video_id, new_values=metadata)
        except:
            os.remove(video_path)
            metadata = {
                "status": "Error",
            }
            self.metadata_handler.update_video_metadata(video_id=video_id, new_values=metadata)
            raise ValueError("Error while processing, check media format")
        
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
        

