import httpx
from sqlalchemy.orm import Session
from app.models import Connection, Endpoint
from app.db import get_db
import asyncio

async def fetch_data(url, method, headers, params, body):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=body if method in ["POST", "PUT"] else None
        )
        return response.json()

async def sync_data(db: Session):
    connections = db.query(Connection).all()
    
    tasks = []
    for connection in connections:
        for endpoint in connection.endpoints:
            url = f"{connection.base_url}{endpoint.path}"
            headers = connection.headers or {}
            params = endpoint.query_params or {}
            body = endpoint.body_params or {}

            tasks.append(fetch_data(url, endpoint.method, headers, params, body))
    
    results = await asyncio.gather(*tasks)
    return results
