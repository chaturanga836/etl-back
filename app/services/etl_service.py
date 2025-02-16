import logging
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.endpoint_repository import EndpointRepository
from app.repositories.api_response_repository import ApiResponseRepository
from app.utils.http_client import HTTPClient  # Import new HTTPClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETLService:
    @staticmethod
    async def add_endpoint(db: AsyncSession, name: str, path: str, method: str, query_params: dict, body_params: dict, base_url: str):
        """Registers an API endpoint for extraction."""
        return await EndpointRepository.add_endpoint(db, name, path, method, query_params, body_params, base_url)

    @staticmethod
    async def extract_data(db: AsyncSession, name: str):
        """Extracts data from an API endpoint."""
        endpoint = await EndpointRepository.get_endpoint_by_name(db, name)
        if not endpoint:
            logger.error(f"Endpoint not found: {name}")
            raise HTTPException(status_code=404, detail="Endpoint not found")

        await db.refresh(endpoint, attribute_names=['base_url'])  # Load base_url relation
        url = endpoint.base_url.base_url + endpoint.path

        logger.info(f"Fetching data from: {url}")
        response_data, status_code, headers = await HTTPClient.fetch(url, endpoint.method, endpoint.query_params, endpoint.body_params)

        # Save API response
        await ApiResponseRepository.save_api_response(db, name, response_data, status_code, headers)

        if status_code != 200:
            raise HTTPException(status_code=status_code, detail="Failed to extract data")

        return response_data

    @staticmethod
    async def transform_data(data: dict):
        """Applies data transformations (modify as needed)."""
        transformed_data = {k.lower(): v for k, v in data.items()}  # Example transformation
        return transformed_data

    @staticmethod
    async def load_data(db: AsyncSession, name: str, transformed_data: dict):
        """Loads transformed data into the database."""
        logger.info(f"Loading transformed data for {name}")
        await ApiResponseRepository.save_api_response(db, name, transformed_data, 200, {})  # Save transformed data

    @staticmethod
    async def process_etl(db: AsyncSession, name: str):
        """Runs the full ETL process for a single endpoint."""
        extracted_data = await ETLService.extract_data(db, name)
        transformed_data = await ETLService.transform_data(extracted_data)
        await ETLService.load_data(db, name, transformed_data)
        return {"message": "ETL process completed", "data": transformed_data}

    @staticmethod
    async def process_multiple_etl(db: AsyncSession, names: list):
        """Processes ETL for multiple endpoints in parallel."""
        tasks = [ETLService.process_etl(db, name) for name in names]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
