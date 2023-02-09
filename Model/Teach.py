from pydantic import BaseModel

class Teach(BaseModel):
    id:int
    timeTableID:int
    teacherID:int
    