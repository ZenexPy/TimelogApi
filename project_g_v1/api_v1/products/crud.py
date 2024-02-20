from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.models import Product
from sqlalchemy.engine import Result


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = []
    return products
