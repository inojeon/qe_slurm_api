from pydantic import BaseModel
from enum import Enum


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool


class JobBase(BaseModel):
    shot: int
    input_file: str


class InputTypeEnum(str, Enum):
    qasm = "qasm"


class JobId(BaseModel):
    id: int


class JobUUID(BaseModel):
    uuid: str


class JobUpdateStatus(BaseModel):
    uuid: str
    status: str


class JobUpdateResultfile(BaseModel):
    uuid: str
    status: str
    result_file: str


class JobCreate(BaseModel):
    shot: int
    input_file: str
    type: InputTypeEnum = InputTypeEnum.qasm

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "type": "qasm",
                    "shot": 1024,
                    "input_file": 'OPENQASM 2.0; \ninclude "qelib1.inc"; \nqreg q[3]; \ncreg c[3]; \nrx(1.0) q[0]; \nry(0) q[0]; \nh q[0]; \ncx q[0], q[1]; \nz q[0]; \nmeasure q[0] -> c[0]; \nmeasure q[1] -> c[1]; \nmeasure q[2] -> c[2];',
                }
            ]
        }
    }
