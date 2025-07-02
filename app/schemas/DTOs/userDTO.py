from pydantic import BaseModel, Field

class UserDTO(BaseModel):
    username:str = Field(...,min_length=1, max_length=100, description='User name')
    password:str = Field(..., min_length=4, max_length=20, description="the password must be at least 4 characters and maximum 20")

    class Config:
        from_attributes = True