from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG_MODE,
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    return """
        <html>
            <body>
                <p>Welcome to FastAPI Async Demo!</p>
                <p>For SwaggerUI go to <a href="http://localhost:8080/docs">docs</a></p>
                <p>For PGAdmin go <a href="http://localhost:5050">here</a></p>
            </body>
        </html>
    """
