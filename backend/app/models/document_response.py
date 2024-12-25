from pydantic import BaseModel
from typing import Optional, List


class DocumentResponse(BaseModel):
    """
    Schema for the documentation response model.
    """
    docstring: Optional[List[str]]
    readme: Optional[List[str]]
    overview: Optional[List[str]]
    comments: Optional[List[str]] = None

    class Config:
        """
        Additional configuration options.
        """

        scheme_extra = {
            "example": {
                "docstring": ["This is the documentation response."],
                "readme": ["This is the readme response."],
                "overview": ["This is the overview response."],
                "comments": ["This is the comments response."],
            }
        }
