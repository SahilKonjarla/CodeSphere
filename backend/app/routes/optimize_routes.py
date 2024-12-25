from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.optimize_service import process_optimize_request
from app.models.optimize_response import OptimizeResponse

# Initialize the router for debugging routes
optimize_router = APIRouter()


class OptimizeRequest(BaseModel):
    code: str  # The code snippet to optimize
    # How the user wants to optimize the code inputted
    goal: str = "Looking at the code given. Please improve either the structure, memory usage, or runtime"
    user_id: str  # The user id


@optimize_router.post("/api/v1/optimize", response_model=OptimizeResponse)
async def optimize_code(request: OptimizeRequest):
    """

    :param request: the code and the goal from the user, but the goal is optional
    :return: The optimization results from the agent
    """
    try:
        # Call the service layer to process the optimization results
        result = process_optimize_request(request.user_id, request.code, request.goal)

        # Return the optimization results
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred in server: {str(e)}"
        )