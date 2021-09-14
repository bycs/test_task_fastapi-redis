from pydantic import BaseModel


class ResponseStatusSchema(BaseModel):
    status: str


class VisitedDomainsSchema(BaseModel):
    domains: list[str]
    status: str
