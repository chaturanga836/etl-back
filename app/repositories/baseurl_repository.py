from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.endpoint import BaseURL  # Import BaseURL from endpoint

class BaseURLRepository:

    @staticmethod
    async def get_or_create_base_url(db: AsyncSession, url: str) -> BaseURL:
        result = await db.execute(select(BaseURL).filter(BaseURL.base_url == url))
        base_url = result.scalars().first()
        if not base_url:
            base_url = BaseURL(base_url=url)
            db.add(base_url)
            await db.commit()
            await db.refresh(base_url)
        return base_url
