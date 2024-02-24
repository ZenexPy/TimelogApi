from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from ..core.models.models import Product as Product_model

from .schemas import Product, ProductBase, ProductUpdatePartial


async def get_products(session: AsyncSession) -> list[Product_model]:
    stmt = select(Product_model).order_by(Product_model.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(product_id: int, session: AsyncSession) -> Product_model | None:
    return await session.get(Product_model, product_id)


async def create_product(session: AsyncSession, product_in: ProductBase) -> Product_model:
    product = Product_model(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product


async def update_product(session: AsyncSession, product: Product, product_update: ProductBase | ProductUpdatePartial, partial: bool = False) -> Product_model:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: Product) -> None:
    await session.delete(product)
    await session.commit()
