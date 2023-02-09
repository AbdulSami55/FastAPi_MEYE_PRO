
from pydantic import BaseModel

class Study(BaseModel):
    id:int
    teachID:int
    eid:int