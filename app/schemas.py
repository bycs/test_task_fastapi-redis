from pydantic import AnyUrl, BaseModel


class ResponseStatusSchema(BaseModel):
    """Схема pydantic для проверки ответа от visited_links_post"""

    status: str


class RequestsVisitedLinksSchema(BaseModel):
    """Схема pydantic для проверки запроса для visited_domains_get"""

    links: list[AnyUrl]


class VisitedDomainsSchema(BaseModel):
    """Схема pydantic для проверки ответа от visited_domains_get"""

    domains: list[str]
    status: str


class UrlSchema(BaseModel):
    """Схема pydantic для проверки url"""

    url: AnyUrl
