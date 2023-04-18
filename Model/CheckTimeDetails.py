
from pydantic import BaseModel
from datetime import datetime

class CheckTimeDetails(BaseModel):
    id:int
    checkTimeID:int
    timein:datetime
    timeout:datetime
    sit:int
    stand:int
    mobile:int
    

class TeacherCHRDetails(BaseModel):
    courseName:str
    day:str
    discipline:str
    startTime:str
    endTime:str
    totalTimeIn:str
    totalTimeOut:str
    timein:datetime
    timeout:datetime
    sit:int
    stand:int
    mobile:int
    status:str