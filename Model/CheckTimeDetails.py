
from typing import List
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
    

class TeacherCHRActivityDetails(BaseModel):
    timein:datetime
    timeout:datetime
    sit:int
    stand:int
    mobile:int
    
class TeacherCHRDetails(BaseModel):
    id:int
    courseName:str
    day:str
    discipline:str
    startTime:str
    endTime:str
    totalTimeIn:str
    totalTimeOut:str
    status:str
    date:str
    teacherCHRActivityDetails:List[TeacherCHRActivityDetails]