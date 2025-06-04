"""
The hello-restful api

An example of a RESTful API written in Python using FastAPI. Modeled after httobin,
but with some api resources definitions useful for misc mocks and other testing.
"""

from typing import Dict
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from .routes import inspection, status, methods, file_response, healthz, istio
from .config import settings, route_prefix

tags_metadata = [
    {"name": "main"},
    {
        "name": "status codes",
        "description": "Return desired status code from any method.",
    },
    {"name": "request inspection", "description": "View elements in the request."},
    {"name": "example resource", "description": "Simulated employee list."},
    {"name": "response formats", "description": "Return different file formats."},
]

api = FastAPI(
    title=settings.title,
    description=settings.description,
    version=settings.releaseId,
    openapi_tags=tags_metadata,
    docs_url=f"{route_prefix}/apidocs",
    openapi_url=f"{route_prefix}/openapi.json",
    redoc_url=None,
    debug=settings.debug,
)

api.include_router(inspection.route, prefix=route_prefix)
api.include_router(status.route, prefix=route_prefix)
api.include_router(methods.route, prefix=route_prefix)
api.include_router(file_response.route, prefix=route_prefix)
api.include_router(healthz.route, prefix=route_prefix)
api.include_router(istio.route, prefix=route_prefix)


@api.get(route_prefix, summary="greeting", tags=["main"])
async def root() -> Dict[str, str]:
    """
    root endpoint and hello response.
    """
    return {"message": "Hello Restful!"}


FastAPIInstrumentor.instrument_app(api)
