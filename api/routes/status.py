"""
hello-restful api

This module defines a FastAPI router that demonstrates how to return responses
with arbitrary HTTP status codes across all standard HTTP methods.

Supports custom responses for 2xx, 3xx, 4xx, and 5xx codes.
For 204 and 304 responses, the endpoint omits the body to comply with HTTP specifications.
"""

from fastapi import APIRouter, Path, Response
from pydantic import BaseModel


# pylint: disable=too-few-public-methods
class Message(BaseModel):
    """A simple response schema containing a textual status message."""

    message: str


responses = {
    200: {"model": Message, "description": "Sucess"},
    300: {"model": Message, "description": "Redirection"},
    400: {"model": Message, "description": "Client Errors"},
    500: {"model": Message, "description": "Server Errors"},
}

route = APIRouter()


@route.api_route(
    "/status/{code}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    summary="Return the requested status code.",
    tags=["status codes"],
    responses={**responses},
)
def return_status(
    response: Response,
    code: int = Path(..., title="Status code to return.", ge=200, le=599),
) -> dict:
    """
    Return a response with the specified HTTP status code.

    Parameters:
        code (int): The HTTP status code to return in the response.
            Must be between 200 and 599 inclusive.

    Behavior:
        - For codes 204 (No Content) and 304 (Not Modified), the response will have no body.
        - For all other status codes, a JSON response containing a 'message' field is returned.

    Returns:
        StatusMessage | Response: A Pydantic model with a message field or an empty Response.
    """
    response.status_code = code
    return {"message": code}
