from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Role(Enum):
    ROLE_1 = 'Teacher'
    ROLE_2 = 'Admin'
    ROLE_3 = 'Student'

class User(BaseModel):
    id:int
    uid:str
    name:str
    image:Optional[str] = None
    password:str
    role:Role