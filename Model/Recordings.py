
from pydantic import BaseModel

class Recordings(BaseModel):
    courseCode:str
    courseName:str
    teacherName:str
    discipline:str
    venue:str
    day:str
    startTime:str
    endTime:str
    date:str
    status:str
    slot:int
    fileName:str
