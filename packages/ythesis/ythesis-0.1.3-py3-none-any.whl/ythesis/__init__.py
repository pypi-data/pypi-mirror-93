from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional


@dataclass(frozen=True)
class Thesis:
    title: str
    authors: Iterable[str]
    published: datetime
    journal_name: str
    url: str
    updated: Optional[datetime] = None
