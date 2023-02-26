from pydantic import BaseModel

class Enroll(BaseModel):
    id:int
    courseCode:int
    studentID:int