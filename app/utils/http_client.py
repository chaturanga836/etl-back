import httpx
import logging

logger = logging.getLogger(__name__)

class HTTPClient:
    @staticmethod
    async def fetch(url: str, method: str = "GET", params: dict = None, body: dict = None):
        """Handles API requests asynchronously."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method=method, url=url, params=params, json=body)
                response.raise_for_status()  # Raise error for 4xx/5xx status codes
                return response.json(), response.status_code, dict(response.headers)
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return {"error": "HTTP error", "message": e.response.text}, e.response.status_code, {}
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            return {"error": "Request failed", "message": str(e)}, 500, {}
