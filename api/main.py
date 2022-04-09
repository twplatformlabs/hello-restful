from fastapi import FastAPI
from .routes import inspection, status, methods

tags_metadata = [
    {
        "name": "main"
    },
    {
        "name": "status codes",
        "description": "Return desired status code from any method."
    },
        {
        "name": "request inspection",
        "description": "View elements in the request."
    }
]

description = """
### Lightweight restul api simulator and testing endpoint.
[Repository](https://github.com/ThoughtWorks-DPS/hello-restful)
"""

api = FastAPI(
    title="hello-restful",
    description=description,
    version="0.0.1",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=tags_metadata,
    docs_url="/apidocs", redoc_url=None
)

api.include_router(inspection.route)
api.include_router(status.route)
api.include_router(methods.route)

@api.get("/", summary="greeting", tags=["main"])
async def root():
    return {"message": "Hello Restful!"}