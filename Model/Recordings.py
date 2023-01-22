
from pydantic import BaseModel

class Recordings(BaseModel):
    id:int
    tsid:int
    filename:str
    date:str
    