import http
import json
import os
from datetime import datetime
from typing import Union

import aioredis

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

import tldextract

from .schemas import (
    RequestsVisitedLinksSchema,
    ResponseStatusSchema,
    ResponseVisitedDomainsSchema,
)


app = FastAPI()

redis_client = aioredis.from_url(
    f'redis://{os.getenv("REDIS_HOST")}',
    port=os.getenv("REDIS_PORT"),
    db=os.getenv("REDIS_DB"),
    password=os.getenv("REDIS_PASSWORD"),
    encoding="utf-8",
    decode_responses=True,
)


def url_parsing(url: str) -> str:
    extract_result = tldextract.extract(url)
    domain = f"{extract_result.domain}.{extract_result.suffix}"
    return domain


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(
        json.dumps({"status": http.HTTPStatus.BAD_REQUEST.phrase}), status_code=400
    )


@app.post(
    "/visited_links",
    response_model=ResponseStatusSchema,
    status_code=status.HTTP_200_OK,
)
async def visited_links_post(
    json_links: RequestsVisitedLinksSchema,
) -> Union[ResponseStatusSchema, PlainTextResponse]:
    """Передача в сервис массива ссылок в POST-запросе.
    Временем их посещения считается время получения запроса сервисом.
    Формат даты - Unix time."""

    datetime_now = datetime.utcnow().timestamp()
    for link in json_links.links:
        try:
            await redis_client.zadd(
                name="links", mapping={url_parsing(link): datetime_now}
            )
            await redis_client.close()
        except ConnectionError:
            return PlainTextResponse(
                json.dumps({"status": http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase}),
                status_code=500,
            )
    status_detail = http.HTTPStatus.OK.phrase
    return {"status": status_detail}


@app.get(
    "/visited_domains",
    response_model=ResponseVisitedDomainsSchema,
    status_code=status.HTTP_200_OK,
)
async def visited_domains_get(
    datetime_from: Union[int, float], datetime_to: Union[int, float]
) -> Union[ResponseVisitedDomainsSchema, PlainTextResponse]:
    """Получение GET-запросом списка уникальных доменов,
    посещенных за переданный интервал времени.
    Формат даты - Unix time."""

    try:
        domains = await redis_client.zrangebyscore(
            name="links", min=datetime_from, max=datetime_to
        )
        await redis_client.close()
    except ConnectionError:
        return PlainTextResponse(
            json.dumps({"status": http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase}),
            status_code=500,
        )
    else:
        status_detail = http.HTTPStatus.OK.phrase
        return {"domains": list(set(domains)), "status": status_detail}
