from pydantic import BaseModel

class Course(BaseModel):
    id:int
    courseCode:str
    courseName:str