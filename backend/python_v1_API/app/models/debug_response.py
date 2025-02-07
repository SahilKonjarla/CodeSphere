from pydantic import BaseModel
from typing import List


class DebugResponse(BaseModel):
    """
    Schema for the debug response.
    """
    errors: List[str]
    suggestions: List[str]
    explanation: List[str]

    class Config:
        """
        Additional configuration options.
        """
        schema_extra = {
            "example": {
                "errors": ["Syntax error on line 5: Unexpected token '='"],
                "suggestions": ["Replace '=' with '==' for comparison"],
                "explanation": [
                    "The code attempted to use '=' in a conditional statement, "
                    "which is invalid syntax. Use '==' for comparisons."
                ]
            }
        }