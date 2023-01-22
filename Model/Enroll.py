from pydantic import BaseModel

class Enroll(BaseModel):
    id:int
    cid:int
    sid:int