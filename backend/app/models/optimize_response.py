from pydantic import BaseModel
from typing import List, Optional


class OptimizeResponse(BaseModel):
    """
    Schema for the optimize response.
    """
    inefficiencies: List[str]
    suggestions: List[str]
    explanation: List[str]

    class Config:
        """
        Additional configuration options.
        """
        schema_extra = {
            "example": {
                "inefficiencies": ["There are some structural errors when you are iterating through the loop"],
                "suggestions": ["Instead of a double for loop use the two pointer implementation"],
                "explanation": [
                    "The code is having some runtime issues when using the double for loop"
                ]
            }
        }
