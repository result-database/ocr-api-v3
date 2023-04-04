from db import Base
from sqlalchemy import String, Boolean, Integer, Column,Text, ForeignKey
from sqlalchemy.orm import relationship

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    def __repr__(self):
        return f'<Item name={self.name}>'

class Music(Base):
    __tablename__ = 'musics'
    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(255), nullable=False, unique=False)
    pronunciation = Column(String(255), nullable=False, unique=False)
    creator = Column(String(255), nullable=False, unique=False)
    lyricist = Column(String(255), nullable=False, unique=False)
    composer = Column(String(255), nullable=False, unique=False)
    arranger = Column(String(255), nullable=False, unique=False)
    hash = Column(String(255), unique=False)
    difficulties = relationship("Difficult", back_populates="music")

    def toDict(self):
        return {
            'id': self.id,
            "title": self.title,
            "pronunciation": self.pronunciation,
            "creator": self.creator,
            "lyricist": self.lyricist,
            "composer": self.composer,
            "arranger": self.arranger,
            "hash": self.hash
        }

class Difficult(Base):
    __tablename__ = 'difficulties'
    id = Column(Integer, primary_key=True, autoincrement=False)
    musicId = Column(Integer, ForeignKey('musics.id'), nullable=False)
    musicDifficulty = Column(String(255), nullable=False, unique=False)
    playLevel = Column(Integer, nullable=False, unique=False)
    totalNoteCount = Column(Integer, nullable=False, unique=False)
    music = relationship('Music', back_populates='difficulties')