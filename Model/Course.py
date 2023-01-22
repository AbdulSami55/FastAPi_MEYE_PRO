from pydantic import BaseModel

class Course(BaseModel):
    id:int
    cid:str
    cr_hr:int
    name:str