from typing import Literal
from pydantic import BaseModel, Field

class RequestUnderstanding(BaseModel):
    intent: Literal["learn", "review", "debug"]
    target_concept :str = Field(
        description="The concise concept the user is asking about"
    )
