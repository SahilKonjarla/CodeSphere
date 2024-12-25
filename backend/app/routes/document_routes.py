from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.models.document_response import DocumentResponse
from app.services.document_service import (
    process_docstring_request,
    process_comments_request,
    process_overview_request,
    process_readme_request,
)

# Initialize the router for document routes
document_router = APIRouter()


# Define the request model
class DocumentRequest(BaseModel):
    code: str  # The code snippet to document
    user_id: str  # The user id


# Define the /api/v1/document/docstring endpoint
@document_router.post("/api/v1/document/docstring", response_model=DocumentResponse)
async def document_code(request: DocumentRequest):
    """
    Accepts a code snippet and the documentation type and returns the corresponding documentation type.
    :param request: code and documentation type
    :return: LLM results
    """

    try:
        # Call the service layer to process the documentation request
        result = process_docstring_request(request.user_id, request.code)

        # Return the documentation results as a structured response
        return result
    except ValueError as e:
        # Handle cases where the service raises an error (e.g., invalid input)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Handle unexpected error gracefully
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Define the /api/v1/document/comments endpoint
@document_router.post("/api/v1/document/comments", response_model=DocumentResponse)
async def document_code(request: DocumentRequest):
    """
    Accepts a code snippet and the documentation type and returns the corresponding documentation type.
    :param request: code and documentation type
    :return: LLM results
    """

    try:
        # Call the service layer to process the documentation request
        result = process_comments_request(request.user_id, request.code)

        # Return the documentation results as a structured response
        return result
    except ValueError as e:
        # Handle cases where the service raises an error (e.g., invalid input)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Handle unexpected error gracefully
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Define the /api/v1/document/overview endpoint
@document_router.post("/api/v1/document/overview", response_model=DocumentResponse)
async def document_code(request: DocumentRequest):
    """
    Accepts a code snippet and the documentation type and returns the corresponding documentation type.
    :param request: code and documentation type
    :return: LLM results
    """

    try:
        # Call the service layer to process the documentation request
        result = process_overview_request(request.user_id, request.code)

        # Return the documentation results as a structured response
        return result
    except ValueError as e:
        # Handle cases where the service raises an error (e.g., invalid input)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Handle unexpected error gracefully
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Define the /api/v1/document/readme endpoint
@document_router.post("/api/v1/document/readme", response_model=DocumentResponse)
async def document_code(request: DocumentRequest):
    """
    Accepts a code snippet and the documentation type and returns the corresponding documentation type.
    :param request: code and documentation type
    :return: LLM results
    """

    try:
        # Call the service layer to process the documentation request
        result = process_readme_request(request.user_id, request.code)

        # Return the documentation results as a structured response
        return result
    except ValueError as e:
        # Handle cases where the service raises an error (e.g., invalid input)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Handle unexpected error gracefully
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
