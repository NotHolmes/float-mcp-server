from float_api import FloatAPI
from src.utils import setup_logging
from src.routers.schema import LoggedTimeCreate

logger = setup_logging()


class FloatClient:
    def __init__(
        self, access_token: str, application_name: str, contact_email: str
    ) -> None:
        self.float_client = FloatAPI(access_token, application_name, contact_email)

    def get_people_id(self, email: str) -> int:
        """Fetch the people ID from the Float API.

        Returns:
            int: Sample people ID
        """
        people = self.float_client._get(
            "people",
            [],
            {"email": email, "fields": "people_id,name,email"},
        )

        logger.info(
            f"Fetched people from Float API: {people}",
            extra={"people": people},
        )

        if people:
            return people[0]["people_id"]
        else:
            logger.exception(
                "No people found for the given email.", extra={"email": email}
            )
            raise ValueError("No people found for the given email.")

    def get_logged_time(
        self, people_id: int, start_date: str = None, end_date: str = None
    ) -> dict:
        """Fetch logged time entries for a specific person.

        Args:
            people_id (int): The ID of the person to fetch logged time for.
            start_date (str, optional): Start date in ISO format. Defaults to None.
            end_date (str, optional): End date in ISO format. Defaults to None.

        Returns:
            dict: Logged time entries.
        """
        return self.float_client._get(
            "logged-time",
            [],
            {
                "people_id": people_id,
                "start_date": start_date,
                "end_date": end_date,
                "fields": "logged_time_id,project_id,date,hours,notes,task_id,task_name,billable,locked,created",
            },
        )

    def create_logged_time(self, body: LoggedTimeCreate) -> dict:
        """Log time for a person.

        Args:
            body (LoggedTimeCreate): The logged time entry to create.

        Returns:
            dict: The created logged time entry.
        """
        return self.float_client._post(
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
