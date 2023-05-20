from pydantic import BaseModel

class CheckTime(BaseModel):
    id:int
    teacherSlotID:int
    totaltimein:int
    totaltimeout:int
    date:str
    