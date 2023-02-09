
from pydantic import BaseModel

class Recordings(BaseModel):
    id:int
    teacherSlotID:int
    filename:str
    date:str
    