from pydantic import BaseModel, ConfigDict
from typing import List


from schemas.userResponse import UserResponse


class UsersResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    users: List[UserResponse]
    total: int
    limit: int
    offset: int
    total_pages: int