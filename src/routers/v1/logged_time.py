from fastapi import APIRouter, status, Body
from fastapi.responses import JSONResponse
import httpx
import os

from src.utils import setup_logging
from src.routers.schema import LoggedTimeCreate, LoggedTimeResponse

logger = setup_logging()


BASE_ENDPOINT = "https://api.float.com/v3"
FLOAT_ACCESS_TOKEN = os.getenv("FLOAT_ACCESS_TOKEN")
TEST_EMAIL = os.getenv("TEST_EMAIL")

router = APIRouter(
    responses={
        200: {
            "description": "Successfully created logged time entry",
            "content": {
                "application/json": {
                    "example": {
                        "logged_time_id": "abc123",
                        "people_id": 1,
                        "date": "2025-06-26",
                        "reference_date": None,
                        "hours": 8.0,
                        "billable": 1,
                        "notes": "Worked on feature X",
                        "project_id": 42,
                        "phase_id": 0,
                        "task_id": None,
                        "task_name": None,
                        "task_meta_id": None,
                        "locked": 0,
                        "locked_date": None,
                        "created": "2025-06-26T10:52:21Z",
                        "created_by": 1,
                        "modified": "2025-06-26T10:52:21Z",
                        "modified_by": 1,
                    }
                }
            },
        }
    },
)


async def get_people_id(email: str) -> int:
    """Fetch the people ID from the Float API.

    Returns:
        int: Sample people ID
    """
    logger.info(
        f"Request to Float API: {BASE_ENDPOINT}/people?email={email}",
        extra={"email": email},
    )

    async with httpx.AsyncClient(
        headers={
            "Authorization": f"Bearer {FLOAT_ACCESS_TOKEN}",
        }
    ) as client:
        api_response = await client.get(f"{BASE_ENDPOINT}/people?email={email}")
        response = api_response.json()

    if response:
        return response[0]["people_id"]
    else:
        logger.exception(f"No people found for email: {email}")
        raise ValueError("No people found for the provided email.")


@router.get(
    "/logged-time", response_model=LoggedTimeResponse, status_code=status.HTTP_200_OK
)
async def get_logged_time() -> JSONResponse:
    """Get a logged time entry.

    Returns:
        JSONResponse: 200 status with the logged time entry
    """

    people_id = await get_people_id(TEST_EMAIL)

    logger.info(
        f"Fetching logged time for people_id: {people_id}",
        extra={"people_id": people_id},
    )

    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {FLOAT_ACCESS_TOKEN}"}
    ) as client:
        api_response = await client.get(
            f"{BASE_ENDPOINT}/logged-time?people_id={people_id}"
        )
        response = api_response.json()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response,
    )


@router.post(
    "/logged-time", response_model=LoggedTimeResponse, status_code=status.HTTP_200_OK
)
async def create_logged_time(
    body: LoggedTimeCreate = Body(
        ...,
        example={
            "people_id": 1,
            "date": "2025-06-26",
            "reference_date": None,
            "hours": 8.0,
            "notes": "Worked on feature X",
            "project_id": 42,
            "phase_id": 0,
            "task_id": None,
            "task_name": None,
            "task_meta_id": None,
        },
    ),
) -> JSONResponse:
    """Log time for a person.

    Returns:
        JSONResponse: 200 status with the created logged time entry
    """
    response = {
        "logged_time_id": "abc123",
        **body.dict(),
        "billable": 1,
        "locked": 0,
        "locked_date": None,
        "created": "2025-06-26T10:52:21Z",
        "created_by": 1,
        "modified": "2025-06-26T10:52:21Z",
        "modified_by": 1,
    }
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response,
    )
