from pymongo import MongoClient
import os
from datetime import datetime
from ...schemas.video import VideoMetadata, MatchingJobData
from uuid import UUID

# database_path = os.environ["DATABASE_ADDRESS"]
database_path = "127.0.0.1:27017/"
database_name = "metadata"

# client = MongoClient(f"mongodb://root:example@{database_path}", uuidRepresentation='standard')
# db = client[database_name]

# db.videos.create_index("domain_name", unique=True, partialFilterExpression={"domain_name": {"$exists": True}})

class MetadataHandler:

    def __init__(self, database_path="127.0.0.1:27017/", database_name="metadata"):
        self.client = MongoClient(f"mongodb://root:example@{database_path}", uuidRepresentation='standard')
        self.db = self.client[database_name]
        self.db.videos.create_index("video_id", unique=True, partialFilterExpression={"domain_name": {"$exists": True}})


    def get_video_metadata(self, video_id):
        return self.db.videos.find_one({"video_id": video_id})
    

    def get_all_videos_metadata(self):
        return self.db.videos.find({})


    def add_new_video_metadata(self, video_id):
        video_metadata = VideoMetadata(video_id=video_id,
                                       status="Indexing")
        video_metadata = video_metadata.model_dump()
        self.db.videos.insert_one(video_metadata)


    def update_video_metadata(self, video_id: str, new_values: dict):
        query = {"video_id": video_id}
        new_values = {"$set":new_values}
        self.db.videos.update_one(query, new_values)


    def delete_video_metadata(self, video_id):
        self.db.videos.delete_one({"video_id": video_id})




class JobMetadataHandler:
    def __init__(self, database_path="127.0.0.1:27017/", database_name="metadata"):
        self.client = MongoClient(f"mongodb://root:example@{database_path}", uuidRepresentation='standard')
        self.db = self.client[database_name]
        self.db.indexing_jobs.create_index("job_id", unique=True, partialFilterExpression={"domain_name": {"$exists": True}})


    def submit_matching_job(self, job_id: UUID, video_id: str):
        data = MatchingJobData(
            job_id=job_id,
            query_video_id=video_id,
            status="In progress"
        )
        data = data.model_dump()
        self.db.indexing_jobs.insert_one(data)
    

    def update_matching_job(self, job_id: UUID, new_values: dict):
        query = {"job_id": job_id}
        new_values = {"$set":new_values}
        self.db.indexing_jobs.update_one(query, new_values)


    def get_all_jobs(self):
        return self.db.indexing_jobs.find({})
    

    def get_job_metadata(self, job_id):
        return self.db.indexing_jobs.find_one({"job_id": job_id})


    def get_job_metadata_by_video_id(self, video_id):
        return self.db.indexing_jobs.find({"query_video_id": video_id})
    
    def get_active_jobs(self):
        return self.db.indexing_jobs.find({"status": "In progress"})