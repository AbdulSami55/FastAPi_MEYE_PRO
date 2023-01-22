from pydantic import BaseModel


class Camera(BaseModel):
    id:int
    did:int
    vid:int
    no:str