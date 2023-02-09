from pydantic import BaseModel

class Enroll(BaseModel):
    id:int
    courseID:int
    studentID:int