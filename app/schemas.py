from typing import List

from pydantic import BaseModel


class VisitedDomainsSchema(BaseModel):
    domains: List
    status: str
