import http
import json
import os
from datetime import datetime
from typing import Any, Union

import aioredis

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse


from .schemas import (
    RequestsVisitedLinksSchema,
    ResponseStatusSchema,
    UrlSchema,
    VisitedDomainsSchema,
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
async def visited_links_post(json_links: RequestsVisitedLinksSchema) -> dict[str, Any]:
    """Передача в сервис массива ссылок в POST-запросе.
    Временем их посещения считается время получения запроса сервисом.
    Формат даты - YYMMDDHHDD."""
    datetime_now = datetime.utcnow().strftime("%y%m%d%H%M")
    for link in json_links.links:
        await redis_client.zadd(name="links", mapping={link: datetime_now})
        await redis_client.close()
    status_detail = http.HTTPStatus.OK.phrase
    return {"status": status_detail}


@app.get(
    "/visited_domains",
    response_model=VisitedDomainsSchema,
    status_code=status.HTTP_200_OK,
)
async def visited_domains_get(
    datetime_from: str, datetime_to: str
) -> Union[dict[str, Union[str, list]], PlainTextResponse]:
    """Получение GET-запросом списка уникальных доменов,
    посещенных за переданный интервал времени.
    Формат даты - YYMMDDHHDD."""
    try:
        datetime.strptime(datetime_from, "%y%m%d%H%M")
        datetime.strptime(datetime_to, "%y%m%d%H%M")
    except ValueError:
        return PlainTextResponse(
            json.dumps({"status": http.HTTPStatus.BAD_REQUEST.phrase}), status_code=400
        )
    else:
        links = await redis_client.zrangebyscore(
            name="links", min=datetime_from, max=datetime_to
        )
        await redis_client.close()
        links = (UrlSchema(url=x) for x in links)
        domains = (x.url.host for x in links)
        status_detail = http.HTTPStatus.OK.phrase
        return {"domains": list(set(domains)), "status": status_detail}
