from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.endpoint import Endpoint  # Import Endpoint from endpoint

class EndpointRepository:

    @staticmethod
    async def add_endpoint(db: AsyncSession, name: str, path: str, method: str, query_params: dict, body_params: dict, base_url_id: int) -> Endpoint:
        endpoint = Endpoint(name=name, path=path, method=method, query_params=query_params, body_params=body_params, base_url_id=base_url_id)
        db.add(endpoint)
        await db.commit()
        await db.refresh(endpoint)
        return endpoint

    @staticmethod
    async def get_endpoint_by_name(db: AsyncSession, name: str) -> Endpoint:
        result = await db.execute(select(Endpoint).filter(Endpoint.name == name))
        return result.scalars().first()
