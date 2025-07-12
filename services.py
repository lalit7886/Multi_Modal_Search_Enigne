from models import ContentDetails
from sqlalchemy.orm import Session
from schemas import page_create

def create_page(database: Session, data: page_create):
    
    content_instance = ContentDetails(** data.model_dump())
    database.add(content_instance)
    database.commit()
    database.refresh()
    return content_instance
