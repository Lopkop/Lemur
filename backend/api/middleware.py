import http
import time

from fastapi import Request

from config import logger


async def log_request_middleware(request: Request, call_next):
    """
    This middleware will log all requests and their processing time.
    """
    url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    try:
        status_phrase = http.HTTPStatus(response.status_code).phrase
    except ValueError:
        status_phrase=""

    if response.status_code < 400:
        logger.info(
            f'{host}:{port} - "{request.method} {url}" {response.status_code} '
            f'{status_phrase} {formatted_process_time}ms')
    else:
        logger.error(
            f'{host}:{port} - "{request.method} {url}" {response.status_code} '
            f'{status_phrase} {formatted_process_time}ms')
    return response




    # if response.status_code < 299:
    #     logger.info(
    #         f'{host}:{port} - "{request.method} {url}" {response.status_code} '
    #         f'{status_phrase} {formatted_process_time}ms')
    # else:
    #     logger.error(
    #         f'{host}:{port} - "{request.method} {url}" {response.status_code} '
    #         f'{status_phrase} {formatted_process_time}ms')