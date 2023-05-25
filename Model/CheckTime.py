from pydantic import BaseModel

class CheckTime(BaseModel):
    id:int
    teacherSlotID:int
    totaltimein:int
    totaltimeout:int
    date:str
    sit:int
    stand:int
    mobile:int
    