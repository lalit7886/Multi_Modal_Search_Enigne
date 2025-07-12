
from database import Base
from sqlalchemy import Column, Integer, String, Text

class ContentDetails(Base):
    __tablename__ = "content_details"

    id = Column(Integer, primary_key=True)
    page_url = Column(String(255), nullable=False, unique=True, index=True)
    text_content = Column(Text, nullable=False)
    link_content = Column(Text, nullable=True)

