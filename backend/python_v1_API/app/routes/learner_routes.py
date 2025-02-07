from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.models.learner_response import LearnerResponse
from app.services.learner_service import process_learner_request

# Initialize the router for learner route
learner_router = APIRouter()


# Define the request model
class LearnerRequest(BaseModel):
    user_id: str  # The id of the user


@learner_router.post("/api/v1/learner", response_model=LearnerResponse)
async def learner(request: LearnerRequest):
    """
    Accepts the user id
    :param request: the id of the user
    :return: parsed agent results
    """
    try:
        # Call the service layer to process the learner request
        result = process_learner_request(request.user_id)

        # Return the documentation results as a structured response
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
