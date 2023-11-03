import uuid, os, threading, asyncio, time

from sqlalchemy.orm import Session
from app.db.models import SubmitJob, Jobs, CreateJob, JobUUID, JobUpdateStatus


def create_job_db(db: Session, scriptPath: str, jobUUID: str) -> Jobs:
    db_job = Jobs(scriptPath=scriptPath, uuid=jobUUID)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job


def get_job(db: Session, jobStatus: JobUUID) -> Jobs:
    return db.query(Jobs).filter(Jobs.uuid == jobStatus.uuid).first()


def update_job_db_status(db: Session, jobStatus: JobUpdateStatus):
    job = (
        db.query(Jobs)
        .filter(Jobs.uuid == jobStatus.uuid)
        .update({"status": jobStatus.status})
    )
    db.commit()
    if job:
        return True
    else:
        return False


def check_job_status(slurmJobId: str, jobUUID: str, db: Session):
    while True:
        time.sleep(1)
        job_status = update_job_status(slurmJobId)
        update_job_db_status(
            db=db,
            jobStatus=JobUpdateStatus(uuid=jobUUID, status=job_status),
        )
        if job_status not in ["RUNNING", "PENDING"]:
            return True


def update_job_status(slurmJobId: str):
    print(slurmJobId)
    scontrol_result = (
        os.popen(f"scontrol show job {int(slurmJobId)} | grep JobState").read().strip()
    )

    print(scontrol_result)

    if len(scontrol_result) == 0:
        return False

    job_status = scontrol_result.split(" ")[0].split("JobState=")[1]

    print(job_status)

    return job_status


def create_job(jobInfo: SubmitJob, db: Session) -> CreateJob:
    jobUUID = str(uuid.uuid4())

    create_job_db(db=db, scriptPath=jobInfo.scriptPath, jobUUID=jobUUID)

    job_path = "/".join(jobInfo.scriptPath.split("/")[0:-1])
    os.chdir(job_path)

    print(f"sbatch {jobInfo.scriptPath}")

    return_value = os.popen(f"sbatch {jobInfo.scriptPath}").read()
    print(return_value)
    slurmJobId = return_value.split("Submitted batch job ")[1]

    update_job_db_status(
        db=db,
        jobStatus=JobUpdateStatus(uuid=jobUUID, status="PENDING"),
    )

    t = threading.Thread(target=check_job_status, args=(slurmJobId, jobUUID, db))
    t.start()

    return CreateJob(ok=True, uuid=jobUUID)
