import datetime
from pydantic import BaseModel


class Article(BaseModel):
    id: str
    title: str
    content: str
    location: str
    date: datetime.datetime
    source: str
