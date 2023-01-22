
from pydantic import BaseModel
from datetime import datetime

class CheckTimeDetails(BaseModel):
    id:int
    ctid:int
    timein:datetime
    timeout:datetime