from typing import Optional, List
from datetime import datetime

class User:
    id: Optional[any] = None
    name: str
    email: str
    hashed_password: str
    role: str

    def __init__(self, name, email, hashed_password, role, id=None) -> None:
        if id!=None:
            self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
    
