from ..qdrant_handler import VectorHandler
from ..vectorizer import ResnetVectorizer, AbstractVideoVectorizer
from ..metadata_handler import MetadataHandler
import os
from pathlib import Path
from datetime import datetime


class ProcessingPipeline:

    def __init__(self, 
                 video_vectorizer: AbstractVideoVectorizer, 
                 video_db_handler: VectorHandler,
                 metadata_handler: MetadataHandler):
        
        self.video_vectorizer = video_vectorizer
        self.video_db_handler = video_db_handler
        self.metadata_handler = metadata_handler

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
