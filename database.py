from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

data_base_url = "postgresql://postgres:Unknown%4075@localhost:5432/crawller"

sql_engine = create_engine(data_base_url, echo=True)

session_local = sessionmaker(autocommit=False, autoflush=False,bind=sql_engine)

Base = declarative_base()

def getdb():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
def create_tables():
    Base.metadata.create_all(bind=sql_engine)