from pydantic import BaseModel


class UnisatItem(BaseModel):
    ticker: str
    overallBalance: float
    transferableBalance: float
    availableBalance: float


class UnisatData(BaseModel):
    height: int
    total: int
    start: int
    detail: list[UnisatItem] | None


class UnisatResponse(BaseModel):
    code: int
    msg: str
    data: UnisatData


class UnisatAccount(BaseModel):
    address: str | None
    response: UnisatResponse | None
