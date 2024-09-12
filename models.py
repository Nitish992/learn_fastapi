from pydantic import BaseModel, Field

class UserDataIn(BaseModel):
    name: str
    language: str
    user_id: str = Field(..., alias='id')  
    bio: str
    version: float

    class Config:
        populate_by_name = True

class DataOut(BaseModel):
    user_id: str  
    name: str
    bio: str

    class Config:
        from_attributes = True  
