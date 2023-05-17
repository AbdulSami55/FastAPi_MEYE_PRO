
from typing import List, Optional
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
    timein:Optional[datetime]
    timeout:Optional[datetime]
    sit:Optional[int]
    stand:Optional[int]
    mobile:Optional[int]
    
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
    teacherName:str
    image:str
    teacherCHRActivityDetails:List[TeacherCHRActivityDetails]