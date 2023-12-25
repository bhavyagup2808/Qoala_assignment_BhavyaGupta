from pydantic import BaseModel
from typing import Optional, List, Any

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        json_schema_extra = {
            'example': {
                "name": "manan jain",
                "email": "test@example.com",
                "password": "password123"
            }
        }