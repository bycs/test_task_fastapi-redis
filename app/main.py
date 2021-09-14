import datetime
import http
import os

import aioredis

from fastapi import FastAPI, status

import tldextract

from .schemas import ResponseStatusSchema, VisitedDomainsSchema


def url_parsing(url: str) -> str:
    extract_result = tldextract.extract(url)
    domain = f"{extract_result.domain}.{extract_result.suffix}"
    return domain


app = FastAPI()

redis_client = aioredis.from_url(
    f'redis://{os.getenv("REDIS_HOST")}',
    port=os.getenv("REDIS_PORT"),
    db=os.getenv("REDIS_DB"),
    password=os.getenv("REDIS_PASSWORD"),
    encoding="utf-8",
    decode_responses=True,
)


@app.post(
    "/visited_links",
    response_model=ResponseStatusSchema,
    status_code=status.HTTP_200_OK,
)
async def visited_links_post(links: dict) -> dict:
    datetime_now = datetime.datetime.utcnow().strftime("%y%m%d%H%M")
    links = links["links"]
    for link in links:
        await redis_client.zadd(name="links", mapping={link: datetime_now})
        await redis_client.close()
    status_detail = http.HTTPStatus.OK.phrase
    return {"status": status_detail}


@app.get(
    "/visited_domains",
    response_model=VisitedDomainsSchema,
    status_code=status.HTTP_200_OK,
)
async def visited_domains_get(datetime_from: int, datetime_from_to: int) -> dict:
    domains = await redis_client.zrangebyscore(
        name="links", min=datetime_from, max=datetime_from_to
    )
    await redis_client.close()
    domains = (url_parsing(x) for x in domains)
    status_detail = http.HTTPStatus.OK.phrase
    return {"domains": list(set(domains)), "status": status_detail}
