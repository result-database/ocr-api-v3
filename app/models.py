from db import Base
from sqlalchemy import String, Integer, Column,Text, ForeignKey

class Music(Base):
    __tablename__ = 'musics'
    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(255), nullable=False, unique=False)
    pronunciation = Column(String(255), nullable=False, unique=False)
    creator = Column(String(255), nullable=False, unique=False)
    lyricist = Column(String(255), nullable=False, unique=False)
    composer = Column(String(255), nullable=False, unique=False)
    arranger = Column(String(255), nullable=False, unique=False)

    level_easy = Column(Integer, nullable=True, unique=False)
    level_normal = Column(Integer, nullable=True, unique=False)
    level_hard = Column(Integer, nullable=True, unique=False)
    level_expert = Column(Integer, nullable=True, unique=False)
    level_master = Column(Integer, nullable=True, unique=False)

    totalNote_easy = Column(Integer, nullable=True, unique=False)
    totalNote_normal = Column(Integer, nullable=True, unique=False)
    totalNote_hard = Column(Integer, nullable=True, unique=False)
    totalNote_expert = Column(Integer, nullable=True, unique=False)
    totalNote_master = Column(Integer, nullable=True, unique=False)

    hash = Column(String(255), unique=False)

    def toDict(self):
        return {
            'id': self.id,
            "title": self.title,
            "pronunciation": self.pronunciation,
            "creator": self.creator,
            "lyricist": self.lyricist,
            "composer": self.composer,
            "arranger": self.arranger,
            "level_easy": self.level_easy,
            "level_normal": self.level_normal,
            "level_hard": self.level_hard,
            "level_expert": self.level_expert,
            "level_master": self.level_master,
            "totalNote_easy": self.totalNote_easy,
            "totalNote_normal": self.totalNote_normal,
            "totalNote_hard": self.totalNote_hard,
            "totalNote_expert": self.totalNote_expert,
            "totalNote_master": self.totalNote_master,
            "hash": self.hash
        }
