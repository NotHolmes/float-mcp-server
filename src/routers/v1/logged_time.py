from fastapi import APIRouter, status, Body, Request, Query
from fastapi.responses import JSONResponse

from typing import Annotated
from datetime import date

from src.utils import setup_logging
from src.routers.schema import LoggedTimeCreate, LoggedTimeResponse
from src.float import FloatClient

logger = setup_logging()

router = APIRouter(
    responses={
        200: {
            "description": "Successfully created logged time entry",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "logged_time_id": "685e0d4f4504e5cad0d322ed",
                            "people_id": 18432436,
                            "task_meta_id": 34200865,
                            "task_id": None,
                            "date": "2025-06-27",
                            "reference_date": None,
                            "hours": 4,
                            "notes": "Worked on....",
                            "priority": 0,
                            "modified": "2025-06-27 03:17:35",
                            "modified_by": 1074275,
                            "created": "2025-06-27 03:17:35",
                            "created_by": 1074275,
                            "task_name": "implement",
                            "project_id": 10399965,
                            "phase_id": 0,
                            "billable": 1,
                            "locked": 0,
                            "locked_date": None,
                        }
                    ]
                }
            },
        }
    },
)


@router.get(
    "/logged-time", response_model=LoggedTimeResponse, status_code=status.HTTP_200_OK
)
async def get_logged_time(
    request: Request,
    email: Annotated[str, Query(...)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> JSONResponse:
    """Get a logged time entry.

    Args:
        email (str): The email address to fetch logged time for.

    Returns:
        JSONResponse: 200 status with the logged time entry
    """
    float_client: FloatClient = request.app.state.float_client
    people_id = float_client.get_people_id(email)

    logger.info(
        f"Fetching logged time for people_id: {people_id}",
        extra={"people_id": people_id},
    )

    logged_time = float_client.get_logged_time(people_id, start_date, end_date)

    return JSONResponse(status_code=status.HTTP_200_OK, content=logged_time)


@router.post(
    "/logged-time", response_model=LoggedTimeResponse, status_code=status.HTTP_200_OK
)
async def create_logged_time(
    request: Request,
    body: LoggedTimeCreate = Body(
        ...,
        example={
            "people_id": 1,
            "date": "2025-06-26",
            "hours": 8.0,
            "notes": "Worked on feature X",
            "project_id": 42,
            "task_name": None,
        },
    ),
) -> JSONResponse:
    """Log time for a person.

    Returns:
        JSONResponse: 200 status with the created logged time entry
    """

    float_client: FloatClient = request.app.state.float_client

    logger.info(f"Creating logged time entry for {body}")

    response = float_client.create_logged_time(body=body)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response,
    )
