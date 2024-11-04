from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Quality(Enum):
    """Video quality"""

    P2160 = "2160"
    P1080 = "1080"
    P720 = "720"
    P540 = "540"
    P360 = "360"
    P224 = "224"


class Video(BaseModel):
    """video model"""

    id: Optional[str] = None
    title: str
    m3u8_url: Optional[str]


class Media(BaseModel):
    """media model"""

    name: str
    url: str


class Section(BaseModel):
    """section model"""

    id: Optional[str] = None
    title: str
    videos: list[Video]
    assets: list[Media] = []


class Course(BaseModel):
    """course model"""

    id: Optional[str] = None
    title: str
    sections: list[Section]
    assets: list[Media] = []


class CourseInfo(BaseModel):
    """course info model"""

    title: str
    stats: list[str]
