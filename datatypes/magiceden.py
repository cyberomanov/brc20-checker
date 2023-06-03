from typing import List, Optional

from pydantic import BaseModel


class Attribute(BaseModel):
    value: str | None
    trait_type: str | None


class Collection(BaseModel):
    symbol: str | None
    name: str | None
    imageURI: str | None
    chain: str | None
    inscriptionIcon: str | None
    description: str | None
    supply: int | None
    twitterLink: str | None
    discordLink: str | None
    websiteLink: str | None
    createdAt: str | None


class Meta(BaseModel):
    name: str | None
    attributes: List[Attribute] | None
    high_res_img_url: str | None


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
    contentBody: Optional[str] | None


class MagicResponse(BaseModel):
    total: int | None
    tokens: List[MagicItem] | None


class MagicDecodedItem(BaseModel):
    p: str | None
    op: str | None
    tick: str | None
    amt: int | None
    name: str | None
