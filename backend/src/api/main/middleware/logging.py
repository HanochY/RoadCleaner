from api.main.types.logs.uvicorn import UvicornLog
from api.main.types.logs.request import RequestLog 
from api.main.types.logs.error import ErrorLog
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
#from fastapi.concurrency import iterate_in_threadpool
#from uuid import uuid4
#import json
import logging
import json

logger = logging.getLogger()
async def generate_fastapi_request_log(request: Request) -> RequestLog:
    return RequestLog(
        method = request.method,
        route = request['path'],
        ip = request.client.host,
        url = str(request.url),
        host = request.url.hostname,
        body = str((await request.body()).decode('utf-8')) or '',
        headers = dict(request.headers.items())
    )

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            log = await generate_fastapi_request_log(request)
            logger.info(json.loads(log.model_dump_json()))
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error("%s %s", *ErrorLog(error_message=str(e)).model_dump().values())
            raise
