from pydantic import BaseModel, Field


class UserCreationSchema(BaseModel):
    username: str = Field(max_length=40)
    email: str = Field(max_length=50)
    first_name: str = Field(max_length=40)
    last_name: str = Field(max_length=40)
    password: str = Field(min_length=8, exclude=True)
