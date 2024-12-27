from pydantic import BaseModel
from typing import List


class LearnerResponse(BaseModel):
    """
    Schema for Learner response.
    """
    trends: List[str]
    recommendations: List[str]
    resources: List[str]

    class Config:
        """
        Additional configuration options.
        """
        schema_extra = {
            "example": {
                "trends": ["Frequent syntax errors in Python Loops",
                           "Common requests for performance optimizations"],
                "recommendations": ["use `flake8` for linting python code",
                                    "Learn about generator expressions to optimize loops"],
                "resources": ["[Python Linting with Flake8](https://flake8.pycqa.org)",
                              "[Guide to Python Generators](https://realpython.com/introduction-to-python-generators/)"]
            }
        }
