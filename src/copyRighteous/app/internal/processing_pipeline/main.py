from ..qdrant_handler import VectorHandler
from ..vectorizer import ResnetVectorizer, AbstractVideoVectorizer
from ...internal.yolo_vectorizer import YoloDetector
from ..metadata_handler import MetadataHandler, JobMetadataHandler
import os
from pathlib import Path
from datetime import datetime

from uuid import uuid4
from ..seqfinder import process_matching_results
if os.environ.get("ENABLE_SOUND_MODEL"):
    from ..sound_matcher import compare_audio_of_video_fragments
from ...schemas.video import MatchingData
from qdrant_client.models import ScoredPoint


blob_address = "./data/videos"

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
        
        if search_while_ingestion:
            job_id = uuid4()
            self.job_metadata_handler.submit_matching_job(job_id=job_id,
                                            video_id=video_id)
            
            matched_vectors = self.video_db_handler.query_vectors_batch(result.tolist())
            matching_data = process_matching_results(matched_vectors)
            yolo_matching_data = self.sync_process_with_yolo(video_path)

            matching_data.extend(yolo_matching_data)

            if os.environ.get("ENABLE_SOUND_MODEL"):
                for result in matching_data:
                    sound_similarity_score = compare_audio_of_video_fragments(video_path, 
                                                    f"./data/videos/{result.match_video_id}.mp4",
                                                    starttime1=result.match_start_frame // 10, endtime1=result.match_end_frame // 10,
                                                    starttime2=result.query_start_frame // 10, endtime2=result.query_end_frame // 10)
                    
                    result.sound_similarity_score = sound_similarity_score

            data = {
                "status": "Done",
                "finished_at": datetime.now(),
                "results": list(map(lambda x: x.model_dump(), matching_data))
            }

            self.job_metadata_handler.update_matching_job(job_id,
                                                        new_values=data)   
            
            if matching_data:
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
        matching_data = process_matching_results(matched_vectors, min_length=90)
        return matching_data


    def sync_video_processing_raw(self, video_path: str) -> list[ScoredPoint]:
        result, frames_count, video_time, framerate = self.video_vectorizer.process_video(video_path=video_path)
        matched_vectors = self.video_db_handler.query_vectors_batch(result.tolist())
        return matched_vectors
    

    def sync_process_with_yolo(self, video_path: str) -> list[MatchingData]:
        yolo_matches = self.yolo_vectorizer.process_video_frames(video_path=video_path)
        matching_data = list()
        for yolo_match in yolo_matches:
            results = self.video_db_handler.query_vectors_batch(yolo_match.vectors)
            print(len(results))
            matching = process_matching_results(results=results, min_length=90, input_offset=yolo_match.start)
            matching_data.extend(matching)
        
        return matching_data
    

    def sync_process_with_yolo_raw(self, video_path: str)  -> list[ScoredPoint]:
        yolo_matches = self.yolo_vectorizer.process_video_frames(video_path=video_path)
        matching_data = list()
        for yolo_match in yolo_matches:
            results = self.video_db_handler.query_vectors_batch(yolo_match.vectors)
            matching_data.extend(results)
        
        return results


    def run_video_matching_by_path(self, video_path):
        job_id = uuid4()
        self.job_metadata_handler.submit_matching_job(job_id=job_id,
                                                video_id=Path(video_path).stem)

        results = self.sync_video_processing(video_path=video_path)
        results_yolo = self.sync_process_with_yolo(video_path=video_path)
        results.extend(results_yolo)
        if os.environ.get("ENABLE_SOUND_MODEL"):
            for result in results:
                sound_similarity_score = compare_audio_of_video_fragments(video_path, 
                                                f"./data/videos/{result.match_video_id}.mp4",
                                                starttime1=result.match_start_frame // 10, endtime1=result.match_end_frame // 10,
                                                starttime2=result.query_start_frame // 10, endtime2=result.query_end_frame // 10)
                
                result.sound_similarity_score = sound_similarity_score 
        data = {
            "status": "Done",
            "finished_at": datetime.now(),
            "results": list(map(lambda x: x.model_dump(), results))
        }


        self.job_metadata_handler.update_matching_job(job_id,
                                                    new_values=data)          

    def run_video_matching(self, video_id):
        job_id = uuid4()
        self.job_metadata_handler.submit_matching_job(job_id=job_id,
                                                    video_id=video_id)
        vector_search_results = self.video_db_handler.search_nearest_by_video_id(video_id)
        matching_data = process_matching_results(vector_search_results)

        yolo_matching_data = self.sync_process_with_yolo(video_id)

        matching_data.extend(yolo_matching_data)

        data = {
            "status": "Done",
            "finished_at": datetime.now(),
            "results": list(map(lambda x: x.model_dump(), matching_data))
        }

        self.job_metadata_handler.update_matching_job(job_id,
                                                    new_values=data)

        

