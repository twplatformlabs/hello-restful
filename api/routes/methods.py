"""
hello-restful api

This module defines example CRUD operations on a mock employee resource
using FastAPI. It demonstrates basic validation, path/query parameters,
and common REST patterns.
"""

import copy
from typing import Optional
from fastapi import APIRouter, Response, status, Path
from pydantic import BaseModel, constr, EmailStr, Field, ConfigDict

LETTERS_PLUS_DASH = r"^[a-zA-Z-]+$"
USER_ID_MIN = 100000
USER_ID_MAX = 9999999


# pylint: disable=too-few-public-methods
class UserIn(BaseModel):
    """schema for create-user input body"""

    first_name: constr(min_length=2, max_length=30, pattern=LETTERS_PLUS_DASH)
    last_name: constr(min_length=2, max_length=30, pattern=LETTERS_PLUS_DASH)
    email: EmailStr
    position: constr(min_length=2, max_length=45, pattern=LETTERS_PLUS_DASH)

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


# pylint: disable=too-few-public-methods
class UserUpdate(BaseModel):
    """schema for update-user input body"""

    first_name: Optional[str] = Field(
        None, min_length=2, max_length=30, pattern=LETTERS_PLUS_DASH
    )
    last_name: Optional[str] = Field(
        None, min_length=2, max_length=30, pattern=LETTERS_PLUS_DASH
    )
    email: Optional[EmailStr] | None = None
    position: Optional[str] = Field(
        None, min_length=3, max_length=45, pattern=LETTERS_PLUS_DASH
    )

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


# simulated database
resource_data = {
    "employees": [
        {
            "first_name": "Maria",
            "last_name": "Sanchez",
            "email": "maria@example.com",
            "position": "staff",
            "userid": 101444,
        },
        {
            "first_name": "Quo",
            "last_name": "Chen",
            "email": "quobinchen@domain.com",
            "position": "staff",
            "userid": 1049832,
        },
        {
            "first_name": "Danelle",
            "last_name": "Johnson",
            "email": "danellej@custom.com",
            "position": "manager",
            "userid": 276076,
        },
        {
            "first_name": "Pete",
            "last_name": "Santos",
            "email": "psantos44@social.com",
            "position": "staff",
            "userid": 457221,
        },
    ]
}

route = APIRouter()


@route.get(
    "/resource",
    summary="Return a list of all resources",
    tags=["example resource"],
    status_code=status.HTTP_200_OK,
)
async def get_resource(response: Response, last_name: Optional[str] = None) -> dict:
    """
    Retrieve all resources or filter by last name.

    If a `last_name` query parameter is provided, the function performs
    a case-sensitive search for employees whose last names include the substring.
    Otherwise, all resources are returned.
    """
    if last_name:
        results = search_query(last_name)  # pylint: disable=too-many-function-args
        if results["employees"]:
            response.status_code = status.HTTP_200_OK
            return results
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "no search results"}

    return resource_data


@route.get(
    "/resource/{userid}",
    summary="Return a specific resource by userid",
    tags=["example resource"],
    status_code=status.HTTP_200_OK,
)
def get_resource_userid(
    response: Response,
    userid: int = Path(
        ..., title="Resource userid to return.", ge=USER_ID_MIN, le=USER_ID_MAX
    ),
) -> dict:
    """
    Retrieve a single resource by userid.

    Parameters:
    - userid: The unique numeric identifier for the employee (between 100000 and 9999999).

    Returns:
    - 200 OK with the employee resource if found.
    - 404 Not Found if the userid does not exist in the dataset.
    """
    result = [x for x in resource_data["employees"] if x["userid"] == userid]
    if len(result) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "Resource not found"}

    return result[0]


@route.post(
    "/resource",
    summary="Create new resource",
    tags=["example resource"],
    status_code=status.HTTP_201_CREATED,
)
def post_resource(user: UserIn, response: Response) -> dict:
    """
    Create a new employee resource.

    Validates the request body and ensures the email is not already in use.
    If validation passes, a new employee is created with a mock userid.

    Returns:
    - 201 Created with the new resource.
    - 403 Forbidden if the email is already registered.
    """
    result = [x for x in resource_data["employees"] if x["email"] == user.email]
    if len(result) != 0:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"detail": "supplied email is already in use."}

    # mock creating new resource
    new_user = user.model_dump()
    new_user["userid"] = 509612
    return new_user


@route.put(
    "/resource/{userid}",
    summary="Modify all fields of an existing resource",
    tags=["example resource"],
    status_code=status.HTTP_200_OK,
)
def put_resource_userid(
    user: UserIn,
    response: Response,
    userid: int = Path(..., title="Resource userid to modify.", ge=100000, le=9999999),
) -> dict:
    """
    Replace an existing employee resource.

    Performs a full update (all fields required) for the employee with the
    given userid. If the resource does not exist, an error is returned.

    Returns:
    - 200 OK with the updated resource.
    - 404 Not Found if the userid is invalid.
    """
    # uses a deep copy to avoid modifying the original resource_data
    data_copy = copy.deepcopy(resource_data)
    result = [x for x in data_copy["employees"] if x["userid"] == userid]
    if len(result) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "Resource not found"}

    result[0].update(user.model_dump())
    return result[0]


@route.patch(
    "/resource/{userid}",
    summary="Modify one or more fields of existing resource",
    tags=["example resource"],
    status_code=status.HTTP_200_OK,
)
def patch_resource_userid(
    user: UserUpdate,
    response: Response,
    userid: int = Path(..., title="Resource userid to modify.", ge=100000, le=9999999),
) -> dict:
    """
    Partially update an employee resource.

    Only the fields provided in the request body will be updated.
    The rest will remain unchanged. Requires a valid userid.

    Returns:
    - 200 OK with the updated resource.
    - 404 Not Found if the userid is invalid.
    """
    # uses a deep copy to avoid modifying the original resource_data
    data_copy = copy.deepcopy(resource_data)
    result = [x for x in data_copy["employees"] if x["userid"] == userid]
    if len(result) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "Resource not found"}

    result[0].update(user.model_dump(exclude_unset=True))
    return result[0]


@route.delete(
    "/resource/{userid}",
    summary="Delete a specific resource by userid",
    tags=["example resource"],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_resource_userid(
    response: Response,
    userid: int = Path(..., title="Resource userid to delete.", ge=100000, le=999999),
):
    """
    Delete an employee resource by userid.

    Removes the resource if it exists. No content is returned on success.

    Returns:
    - 204 No Content if deletion is successful.
    - 404 Not Found if the userid does not exist.
    """
    result = [x for x in resource_data["employees"] if x["userid"] == userid]
    if len(result) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "Resource not found"}
    return None


def search_query(last_name) -> dict:
    """
    Helper function to filter employees by last name substring.

    Returns a dictionary of employees whose `last_name` contains the
    provided substring.
    """
    matching = {"employees": []}

    for user in resource_data["employees"]:
        if user["last_name"].find(last_name) != -1:
            matching["employees"].append(user)
    return matching
