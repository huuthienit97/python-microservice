from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from .config import Settings

app = FastAPI(title="API Gateway")
settings = Settings()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Proxy endpoints
@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_endpoint(service: str, path: str, request: Request):
    service_urls = {
        "users": settings.USER_SERVICE_URL,
        "auth": settings.AUTH_SERVICE_URL,
        "products": settings.PRODUCT_SERVICE_URL
    }

    if service not in service_urls:
        raise HTTPException(status_code=404, detail="Service not found")

    target_url = f"{service_urls[service]}/{path}"
    
    # Forward the request
    async with httpx.AsyncClient() as client:
        try:
            body = await request.body()
            headers = dict(request.headers)
            method = request.method
            
            response = await client.request(
                method=method,
                url=target_url,
                content=body,
                headers=headers
            )
            
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
