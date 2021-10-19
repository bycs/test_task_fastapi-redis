from pydantic import BaseModel


class RequestsVisitedLinksSchema(BaseModel):
    """Схема pydantic для проверки запроса для visited_domains_get"""

    links: list[str]


class ResponseStatusSchema(BaseModel):
    """Схема pydantic для проверки ответа от visited_links_post"""

    status: str


class ResponseVisitedDomainsSchema(BaseModel):
    """Схема pydantic для проверки ответа от visited_domains_get"""

    domains: list[str]
    status: str
