from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.orchestrator_service import process_orchestrator_request


# Initialize the router for orchestrator routes
orchestrator_router = APIRouter()


# Define the request model
class OrchestratorRequest(BaseModel):
    code: str
    user_id: str
    task: str
    additional_params: dict


# Define the api/v1/orchestrator endpoint
@orchestrator_router.post("/api/v1/orchestrator")
async def orchestrator(request: OrchestratorRequest):
    """
    Receives information from the frontend and calls the main orchestrator agent
    :param request: The necessary information for the orchestrator
    :return: The response from the agent
    """

    try:
        result = process_orchestrator_request(request)

        # return the orchestrator results as a structured response
        return result
    except ValueError as e:
        # Handle cases where the service raises and error (e.g., invalid input)
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
