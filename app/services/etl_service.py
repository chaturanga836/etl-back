import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException  # Import HTTPException from fastapi
from app.repositories.endpoint_repository import EndpointRepository
from app.repositories.baseurl_repository import BaseURLRepository
from app.repositories.api_response_repository import ApiResponseRepository  # Import the new repository
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETLService:

    @staticmethod
    async def add_endpoint(db: AsyncSession, name: str, path: str, method: str, query_params: dict, body_params: dict, base_url: str):
        base_url_entry = await BaseURLRepository.get_or_create_base_url(db, base_url)
        return await EndpointRepository.add_endpoint(db, name, path, method, query_params, body_params, base_url_entry.id)

    @staticmethod
    async def extract_data(db: AsyncSession, name: str):
        logger.info(f"Extracting data for endpoint: {name}")

        endpoint = await EndpointRepository.get_endpoint_by_name(db, name)
        if not endpoint:
            logger.error(f"Endpoint not found: {name}")
            raise HTTPException(status_code=404, detail="Endpoint not found")

        logger.info(f"Found endpoint: {endpoint}")

        # Explicitly load the base_url relationship within the asynchronous context
        await db.refresh(endpoint, attribute_names=['base_url'])
        logger.info(f"Loaded base_url for endpoint: {endpoint.base_url}")

        # Log the query_params to check their values
        logger.info(f"Query Params: {endpoint.query_params}")

        url = endpoint.base_url.base_url + endpoint.path
        logger.info(f"Constructed URL: {url}")

        async with httpx.AsyncClient() as client:
            response = await client.request(method=endpoint.method, url=url, params=endpoint.query_params, json=endpoint.body_params)
            logger.info(f"Received response with status code: {response.status_code}")

        # Try to parse the response as JSON
        try:
            response_data = response.json()
        except ValueError:
            logger.error("Failed to decode JSON response")
            response_data = {"error": "Failed to decode JSON response", "content": response.text}

        # Save the API response to the database, including headers and status code
        await ApiResponseRepository.save_api_response(db, name, response_data, response.status_code, dict(response.headers))

        if response.status_code != 200:
            logger.error(f"Failed to extract data, status code: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to extract data")

        logger.info("Data extracted and saved successfully")
        return response_data
