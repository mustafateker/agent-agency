"""Actual savings are explicit, signed cash movements, never derived leftovers."""
from pydantic import BaseModel, Field, field_validator

class BirikimIstegi(BaseModel):
    gun: str
    tutar_kurus: int = Field(strict=True)
    not_metni: str | None = Field(default=None, max_length=240)

    @field_validator('tutar_kurus')
    @classmethod
    def sifir_olamaz(cls, tutar: int) -> int:
        if tutar == 0:
            raise ValueError('Birikim hareketi sıfır olamaz.')
        return tutar
