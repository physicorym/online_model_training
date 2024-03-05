
from sqlalchemy.orm import Session
from .models import Model

def create_model(db: Session, model_data: dict):
    db_model = Model(**model_data)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def get_models_by_user(db: Session, user_id: int):
    return db.query(Model).filter(Model.user_id == user_id).all()

def get_model(db: Session, model_id: int):
    return db.query(Model).filter(Model.id == model_id).first()
