from pydantic import BaseModel

class Course(BaseModel):
    id:int
    courseID:str
    creditHours:int
    name:str