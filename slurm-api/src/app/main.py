# main.py
from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session

from app.db import database

from app.libs.jobs import create_job, get_job
from app.db.models import SubmitJob, Base, JobUUID

Base.metadata.create_all(bind=database.engine)
app = FastAPI()


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/job", status_code=status.HTTP_201_CREATED)
async def submit_job(jobInfo: SubmitJob, db: Session = Depends(get_db)):
    return create_job(jobInfo=jobInfo, db=db)


@app.get("/job/{jobUUID}/status/", status_code=status.HTTP_200_OK)
async def check_job_status(jobUUID: str, db: Session = Depends(get_db)):
    return {"status": get_job(db=db, jobStatus=JobUUID(uuid=jobUUID)).status}


@app.get("/")
def read_root():
    return {"title": "Slurm API Server POC"}
