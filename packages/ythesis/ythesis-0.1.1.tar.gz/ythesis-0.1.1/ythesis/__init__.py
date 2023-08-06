from dataclasses import dataclass
from datetime import datetime
from typing import Iterator


@dataclass
class Thesis:
    title: str
    authors: Iterator[str]
    published: datetime
    updated: datetime
    journal_name: str
    url: str
