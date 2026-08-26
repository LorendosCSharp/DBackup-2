from fastapi import FastAPI
from fastapi.routing import APIWebSocketRoute
from fastapi.openapi.utils import get_openapi







# Inject iframe into OpenAPI description
def websocket(api: FastAPI):
    if api.openapi_schema:
        return api.openapi_schema

    openapi_schema = get_openapi(
        title=api.title,
        version=api.version,
        description=api.description,
        routes=api.routes,
    )

    for route in api.routes:
        if isinstance(route, APIWebSocketRoute):
            path = route.path
            openapi_schema["paths"][path] = {
                "get": {
                    "summary": f"WebSocket endpoint: {path}",
                    "responses": {
                        "101": {
                            "description": "Switching Protocols - WebSocket connection established."
                        }
                    },
                    "tags": ["WebSocket"],
                    "externalDocs": {
                    }
                }
            }

    api.openapi_schema = openapi_schema
    api.openapi = lambda: openapi_schema
    return api.openapi_schema
