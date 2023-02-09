from enum import Enum
from pydantic import BaseModel

class Day(Enum):
    DAY_1 = 'Mon'
    DAY_2 = 'Tue'
    DAY_3 = 'Wed'
    DAY_4 = 'Thu'
    DAY_5 = 'Fri'

class StartTime(Enum):
    TIME_1 = '08:30'
    TIME_2 = '10:00'
    TIME_3 = '11:30'
    TIME_4 = '01:30'
    TIME_5 = '03:00'
    
class EndTime(Enum):
    TIME_1 = '10:00'
    TIME_2 = '11:30'
    TIME_3 = '01:00'
    TIME_4 = '03:00'
    TIME_5 = '04:30'
    
class TimeTable(BaseModel):
    id : int
    sectionID : int
    starttime : StartTime
    endtime : EndTime
    day:Day
    courseID:int 
    venueID:int   
    