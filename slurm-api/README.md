# api 기능 고민

## get /ws/log/{jobId}

### 절차

- 작업 상태 체크 api 호출
- return running True?
  - get /ws/log/{jobId} 호출
- False
  - get /jobs/log 호출

### 규칙

클라이언트
-> 서버에서는 받은 라인부터 지금까지 생성된 로그 텍스트 내용과 텍스트 마지막 줄 값을 응답으로 보냄

# 슬럼 스크립트 참고자료

https://hpc.stat.yonsei.ac.kr/docs/

https://dandyrilla.github.io/2017-04-11/jobsched-slurm/

# 슬럼 작업 상태 종류

Status Code Explaination
COMPLETED CD The job has completed successfully.
COMPLETING CG The job is finishing but some processes are still active.
FAILED F The job terminated with a non-zero exit code and failed to execute.
PENDING PD The job is waiting for resource allocation. It will eventually run.
PREEMPTED PR The job was terminated because of preemption by another job.
RUNNING R The job currently is allocated to a node and is running.
SUSPENDED S A running job has been stopped with its cores released to other jobs.
STOPPED ST A running job has been stopped with its cores retained.
