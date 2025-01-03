from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.debug_service import process_debug_request
from app.models.debug_response import DebugResponse

# Initialize the router for debugging routes
debug_router = APIRouter()


# Define the request model
class DebugRequest(BaseModel):
    code: str  # The code snippet to debug
    user_id: str  # id of specific user


# Define the /api/v1/debug endpoint
@debug_router.post("/api/v1/debug", response_model=DebugResponse)
async def debug_code(request: DebugRequest):
    """
    Accepts a code snippet and returns the debugging results from the debug_agent
    """
    try:
        # Call the service layer to process the debugging request
        result = process_debug_request(request.user_id, request.code)

        # Return the debugging results as a structured response
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
