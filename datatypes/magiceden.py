from typing import List, Optional

from pydantic import BaseModel


class Attribute(BaseModel):
    value: str
    trait_type: str


class Collection(BaseModel):
    symbol: str
    name: str
    imageURI: str
    chain: str
    inscriptionIcon: str
    description: str
    supply: int
    twitterLink: str
    discordLink: str
    websiteLink: str
    createdAt: str


class Meta(BaseModel):
    name: str
    attributes: List[Attribute]
    high_res_img_url: str


class MagicItem(BaseModel):
    id: str | None
    contentURI: str | None
    contentType: str | None
    contentPreviewURI: str | None
    sat: int | None
    inscriptionNumber: int | None
    chain: str | None
    meta: Meta | None
    location: str | None
    locationBlockHeight: int | None
    locationBlockTime: str | None
    locationBlockHash: str | None
    output: str | None
    outputValue: int | None
    owner: str | None
    listed: bool | None
    listedPrice: int | None
    collectionSymbol: str | None
    collection: Collection | None
    satName: str | None
    satRarity: str | None
    contentBody: Optional[str]


class MagicResponse(BaseModel):
    total: int
    tokens: List[MagicItem]


class MagicDecodedItem(BaseModel):
    p: str
    op: str
    tick: str
    amt: int
