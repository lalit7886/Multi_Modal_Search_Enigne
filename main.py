from fastapi import FastAPI, HTTPException, Depends
import services, models,schemas
from database import session_local, sql_engine, getdb
from sqlalchemy.orm import Session
from crawller import extract_everything, extract_link, bfs 


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "The Api is running sucessfully"}

@app.get("/pages", response_model=list[schemas.Page])
def get_all_pages(db: Session= Depends(getdb)):
    try:
        pages = services.get_pages(db)
        return pages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/pages", response_model=schemas.Page)
def create_page_details(page: schemas.page_create, db: Session = Depends(getdb)):
    try:
        
        
        return services.create_page(db, page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))