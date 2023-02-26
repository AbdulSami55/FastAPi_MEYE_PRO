
from pydantic import BaseModel

class SectionOffer(BaseModel):
    id:int
    courseOfferId:int
    discipline:str

class SectionOfferDetails(BaseModel):
    courseName:str
    courseCode:str
    discipline:str