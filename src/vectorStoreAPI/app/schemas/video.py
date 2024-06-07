from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional
from typing import Literal



class VideoMetadata(BaseModel):
    video_id: str
    uploaded_at: datetime = Field(default_factory=datetime.now)
    indexed_at: Optional[datetime] = None
    status: Literal["Indexing", "Indexed", "Error"]
    frames_count: Optional[int] = None
    video_time: Optional[timedelta] = None 
    framerate: Optional[int] = None
