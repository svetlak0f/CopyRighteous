from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional
from typing import Literal
from uuid import UUID



class VideoMetadata(BaseModel):
    video_id: str
    uploaded_at: datetime = Field(default_factory=datetime.now)
    indexed_at: Optional[datetime] = None
    status: Literal["Indexing", "Indexed", "Error"]
    frames_count: Optional[int] = None
    video_time: Optional[str] = None 
    framerate: Optional[int] = None


class MatchingData(BaseModel):
    query_start_frame: int
    query_end_frame: int
    query_start_time: str
    query_end_time: str

    match_video_id: str
    match_start_frame: int
    match_end_frame: int
    match_start_time: str
    match_end_time: str

    similarity_score: float

class MatchingDataWithID(MatchingData):
    job_id: UUID


class MatchingJobData(BaseModel):
    job_id: UUID

    query_video_id: str
    status: Literal["In progress", "Done", "Error"]

    started_at: datetime = Field(default_factory=datetime.now)
    finished_at: Optional[datetime] = None

    results: Optional[list[MatchingData]] = None