from float_api import FloatAPI
from src.utils import setup_logging

logger = setup_logging()


def get_people_id(float_client: FloatAPI, email: str) -> int:
    """Fetch the people ID from the Float API.

    Returns:
        int: Sample people ID
    """
    people = float_client._get(
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
        logger.exception("No people found for the given email.", extra={"email": email})
        raise ValueError("No people found for the given email.")
