
from enum import Enum
from pydantic import BaseModel
class STATUS(Enum):
    NotTaken = -1
    NotStart = 0
    Taken = 1
    
class TeacherSlot(BaseModel):
    id:int
    teachID:int
    slot:int
    status:STATUS