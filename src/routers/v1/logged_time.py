from fastapi import APIRouter, status, Body, Request, Query
from fastapi.responses import JSONResponse

from typing import Annotated
from datetime import date

from src.utils import setup_logging
from src.routers.schema import LoggedTimeCreate, LoggedTimeResponse
from float_api import FloatAPI
from src.float import get_people_id

logger = setup_logging()

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
    float_client: FloatAPI = request.app.state.float_client
    people_id = get_people_id(float_client, email)

    logger.info(
        f"Fetching logged time for people_id: {people_id}",
        extra={"people_id": people_id},
    )

    logged_time = float_client._get(
        "logged-time",
        [],
        {
            "people_id": people_id,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "fields": "logged_time_id,project_id,date,hours,notes,task_id,task_name,billable,locked,created",
        },
    )

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

    float_client: FloatAPI = request.app.state.float_client

    logger.info(f"Creating logged time entry for {body}")

    response = float_client._post(
        "logged-time",
        {
            "project_id": body.project_id,
            "date": body.date,
            "hours": body.hours,
            "people_id": body.people_id,
            "notes": body.notes,
            "task_name": body.task_name,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response,
    )
