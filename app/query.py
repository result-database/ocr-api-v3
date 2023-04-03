from sqlalchemy.orm import Session

import models

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def create_item(db: Session, name: str):
    db_item = models.Item(name=name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

