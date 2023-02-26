from pydantic import BaseModel

class OfferedCourse(BaseModel):
    id:int
    sessionId:int
    courseId: int

class OfferedCourseDetails(BaseModel):
    courseName:str
    courseCode:str
    sesssionName:str