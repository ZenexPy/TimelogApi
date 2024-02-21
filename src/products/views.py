from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .schemas import Product, ProductUpdatePartial, ProductBase
from core.db_init import db_init
from .dependencies import get_product_by_id

router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[Product])
async def get_products(session: AsyncSession = Depends(db_init.session_dependency)):
    return await crud.get_product(session=session)


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: Product, session: AsyncSession = Depends(db_init.session_dependency)):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}/", response_model=Product)
async def get_product(
    product=Depends(get_product_by_id),
):
    return product


@router.put("/{product_id}/")
async def update_product(
    product_update: ProductBase,
    product=Depends(get_product_by_id),
    session: AsyncSession = Depends(db_init.session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch("/{product_id}/")
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product=Depends(get_product_by_id),
    session: AsyncSession = Depends(db_init.session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product=Depends(get_product_by_id),
    session: AsyncSession = Depends(db_init.session_dependency)
) -> None:
    return await crud.delete_product(
        session=session,
        product=product,
    )
