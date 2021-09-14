import datetime
import http
import json
import os
import urllib.parse

from fastapi import FastAPI, status

import redis

from .schemas import VisitedDomainsSchema


app = FastAPI()
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=os.getenv("REDIS_DB"),
    password=os.getenv("REDIS_PASSWORD"),
)


@app.post("/visited_links", status_code=status.HTTP_200_OK)
def visited_links_post(links_json: str):
    datetime_now = datetime.datetime.utcnow().strftime("%y%m%d%H%M")
    links = json.loads(links_json)["links"]
    for link in links:
        redis_client.zadd(name="links", mapping={link: datetime_now})
        redis_client.close()
    status_detail = http.HTTPStatus.OK.phrase
    return {"status": status_detail, "links": links}


@app.get(
    "/visited_domains",
    response_model=VisitedDomainsSchema,
    status_code=status.HTTP_200_OK,
)
def visited_domains_get(datetime_from: int, datetime_from_to: int):
    domains = redis_client.zrangebyscore(
        name="links", min=datetime_from, max=datetime_from_to
    )
    domains = (x.decode("UTF-8") for x in domains)
    domains = (urllib.parse.urlsplit(x).netloc for x in domains)
    status_detail = http.HTTPStatus.OK.phrase
    return {"domains": list(domains), "status": status_detail}
