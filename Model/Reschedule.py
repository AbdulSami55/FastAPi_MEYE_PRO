from pydantic import BaseModel

from Model.TimeTable import Day,StartTime,EndTime

class Reschedule(BaseModel):
    id:int
    teachID:int
    venueID:int
    status:bool=False
    starttime : StartTime
    endtime : EndTime
    day:Day