from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import List, Optional
from datetime import datetime
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy import JSON, Column

class WordplayBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    word: str
    translation: str
    tags: Optional[str] = Field(default=None)
    datetime: datetime
    remark: Optional[dict] = Field(default=None, sa_column=Column(JSON))

class Wordplay(WordplayBase, table=True):
    __table_args__ = {'extend_existing': True}
    audio: Optional[bytes] = Field(default=None, sa_column=Column(BLOB, nullable=True))

class WordplayRead(WordplayBase):
    pass

class WordplayDetail(WordplayBase):
    audio: Optional[str] = None  # 将音频字段定义为字符串

# 定义 Pydantic 模型来接收请求数据
class WordIdList(BaseModel):
    word_ids: List[int]