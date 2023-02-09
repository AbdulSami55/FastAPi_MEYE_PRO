
from pydantic import BaseModel
from datetime import datetime

class CheckTimeDetails(BaseModel):
    id:int
    checkTimeID:int
    timein:datetime
    timeout:datetime