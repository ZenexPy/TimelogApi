from fastapi import Path, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from ..core.db_init import db_init
from . import crud
from ..core.models.models import Product as Product_model


async def get_product_by_id(product_id: Annotated[int, Path], session: AsyncSession = Depends(db_init.session_dependency)) -> Product_model:
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )
