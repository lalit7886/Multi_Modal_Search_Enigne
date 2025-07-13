from pydantic import BaseModel, Field
from typing import Annotated, Optional

class Page(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier for the page")]
    page_url: Annotated[str, Field(..., description="URL of the page", example="www.example.com")]
    text_content: Annotated[str, Field(..., description="Text content of the page", example="Example text content")]
    link_content: Annotated[Optional[str], Field(None, description="Link content of the page", example="https://www.example.com/link")]

class page_create(BaseModel):
    
    page_url: Annotated[str, Field(..., description="URL of the page", example="www.example.com")]
    text_content: Annotated[str, Field(..., description="Text content of the page", example="Example text content")]
    link_content: Annotated[Optional[str], Field(None, description="Link content of the page", example="https://www.example.com/link")]

class PageOut(Page):
    class Config:
        from_attributes = True
