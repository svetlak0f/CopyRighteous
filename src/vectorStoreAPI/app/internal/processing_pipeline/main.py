from ..qdrant_handler import VectorHandler
from ..vectorizer import ResnetVectorizer, AbstractVideoVectorizer
import os
from pathlib import Path


class ProcessingPipeline:

    def __init__(self, video_vectorizer: AbstractVideoVectorizer, video_db_handler: VectorHandler):
        self.video_vectorizer = video_vectorizer
        self.video_db_handler = video_db_handler

    def process_video(self, video_path):
        try:
            result = self.video_vectorizer.process_video(video_path=video_path)
        except:
            os.remove(video_path)
            raise ValueError("Error while processing, check media format")
        
        try:
            self.video_db_handler.save_vectors(result.tolist(), video_id=Path(video_path).stem)
        except:
            os.remove(video_path)
            raise RuntimeError("Error while ingestion into database")
