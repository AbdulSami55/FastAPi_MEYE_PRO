from pydantic import BaseModel


class Camera(BaseModel):
    id:int
    dvrID:int
    venueID:int
    portNumber:str
    venueName:str