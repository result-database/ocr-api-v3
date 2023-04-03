from db import Base
from sqlalchemy import String, Boolean, Integer, Column,Text

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    def __repr__(self):
        return f'<Item name={self.name}>'