from pydantic import BaseModel
from datetime import datetime
class Attendance(BaseModel):
    id:int
    enrollId :int 
    date : str
    status : bool
    name:str