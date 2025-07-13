from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

data_base_url = "postgresql://postgres:Unknown%4075@localhost:5432/crawller"

sql_engine = create_engine(data_base_url, echo=True) # ysed to connect sqlalchamey to database

session_local = sessionmaker(autocommit=False, autoflush=False,bind=sql_engine) # session is used to intteract with the database tiemporrayly


Base = declarative_base() # base clasoo to define our database model

def getdb(): # fast api will use to inject the database session into the endpooints
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
def create_tables():
    Base.metadata.create_all(bind=sql_engine)