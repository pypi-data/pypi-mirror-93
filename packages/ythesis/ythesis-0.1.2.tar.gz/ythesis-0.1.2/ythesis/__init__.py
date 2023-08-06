from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Optional


@dataclass
class Thesis:
    title: str
    authors: Iterator[str]
    published: datetime
    journal_name: str
    url: str
    updated: Optional[datetime] = None
