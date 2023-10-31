from pydantic import Field, BaseModel
from typing import Dict

class Music(BaseModel):
    id: int
    title: str
    pronunciation: str
    creator: str
    lyricist: str
    composer: str
    arranger: str
    level_easy: int
    level_normal: int
    level_hard: int
    level_expert: int
    level_master: int
    totalNote_easy: int
    totalNote_normal: int
    totalNote_hard: int
    totalNote_expert: int
    totalNote_master: int

class ReqType(BaseModel):
    url: str = Field(default="http://localhost:8080/static/IMG_8955.png")
    psmScore: int = Field(default=6, enum=[6, 7])
    psmDifficult: int = Field(default=7, enum=[6, 7])
    psmTitle: int = Field(default=11, enum=[6, 7, 11])
    psmJudge: int = Field(default=6, enum=[6, 7])
    borderTitle: int = Field(default=215, ge=215, le=255)
    borderJudge: int = Field(default=230, ge=230, le=255)
    blurScore: bool = Field(default=True)
    blurDifficult: bool = Field(default=True)
    blurTitle: bool = Field(default=True)
    blurJudge: bool = Field(default=True)
    candidateRatio: float = Field(default=0.3)
    candidate: bool = Field(default=True)
