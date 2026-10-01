"""One revisioned ledger per account permits atomic nonnegative balance checks."""
from typing import TypedDict

class BirikimHareketi(TypedDict):
    id: str
    gun: str
    tutar_kurus: int
    not_metni: str | None
