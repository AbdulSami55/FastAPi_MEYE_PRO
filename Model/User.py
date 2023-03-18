from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class Role(Enum):
    ROLE_1 = 'Teacher'
    ROLE_2 = 'Admin'
    ROLE_3 = 'Student'

class User(BaseModel):
    id:int
    userID:str
    name:str
    image:Optional[str] = None
    password:str
    role:Role

class Student(BaseModel):
    aridNo:str
    name:str
    image:str
    password:str
    
class StudentCourses(BaseModel):
    teacherName:str
    courseName:str
    discipline:str
    image:str

