from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import List, Optional
from datetime import datetime
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy import JSON, Column

class Wordplay(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    word: str
    word_translation: str
    example: str
    example_translation: str
    tags: Optional[str] = Field(default=None)
    datetime: datetime
    remark: Optional[dict] = Field(default=None, sa_column=Column(JSON))

# 定义 Pydantic 模型来接收请求数据
class WordIdList(BaseModel):
    word_ids: List[int]