from pydantic import BaseModel


class ExplorerResponse(BaseModel):
    address: str
    confirmed: int
    unconfirmed: int
    utxo: int
    txs: int
    received: int
