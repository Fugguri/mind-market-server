import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class CheckAccessTokenMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            some_attribute: str,
    ):
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        # do something with the request object, for example
        content_type = request.headers.get('Content-Type')
        print(content_type)
        # process the request and get the response
        response = await call_next(request)

        return response
