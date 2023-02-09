from pydantic import BaseModel
from datetime import datetime
class Attendance(BaseModel):
    id:int
    studentid :int 
    date : datetime
    status : bool