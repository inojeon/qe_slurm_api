import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from pydantic import BaseModel, Field
from typing import Union, Optional


class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String)
    status = Column(String, default="Created")
    created_date = Column(DateTime, default=datetime.datetime.now)
    scriptPath = Column


class JobUpdateStatus(BaseModel):
    uuid: str
    status: str


class CreateJob(BaseModel):
    ok: bool
    uuid: Optional[str] = None


class JobUUID(BaseModel):
    uuid: str


class SubmitJob(BaseModel):
    scriptPath: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "scriptPath": "/EDISON2/ddd/ddd/ff",
                }
            ]
        }
    }
