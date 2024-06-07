from pymongo import MongoClient
import os
from datetime import datetime
from ...schemas.video import VideoMetadata

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



