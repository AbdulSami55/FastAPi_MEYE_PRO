from pydantic import BaseModel

class CheckTime(BaseModel):
    id:int
    tsid:int
    totaltimein:int
    totaltimeout:int
    