
from pydantic import BaseModel

class Rules(BaseModel):
    id:int
    th_id:int
    start_record : int
    end_record:int
    full_record :int