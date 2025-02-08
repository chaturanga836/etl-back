from sqlalchemy.ext.asyncio import AsyncSession
from app.models.api_response import ApiResponse

class ApiResponseRepository:

    @staticmethod
    async def save_api_response(db: AsyncSession, endpoint_name: str, response_data: dict, status_code: int, headers: dict):
        api_response = ApiResponse(
            endpoint_name=endpoint_name,
            response_data=response_data,
            status_code=status_code,
            headers=headers
        )
        db.add(api_response)
        await db.commit()
        await db.refresh(api_response)
        return api_response
