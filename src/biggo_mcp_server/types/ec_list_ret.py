from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, RootModel


class ModelItem(BaseModel):
    name: str
    # image: str
    # height: str
    # width: str
    # domain: List[str]
    # has_product: bool
    # checkout_url: List[str]
    # checkout_done_url: List[str]
    # image_3x: str = Field(..., alias='image@3x')
    # s3_image: Optional[str] = None
    provide: str
    # s3_logo: Optional[str] = None


class ECListAPIRet(RootModel):
    root: List[ModelItem]
