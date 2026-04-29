from contextlib import asynccontextmanager
import time 
import uvicorn
from fastapi import FastAPI, Request
from src.api.endpoints import router as api_router
from src.core.config import settings
from src.core.logger import logger, setup_logging

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"--- {settings.PROJECT_NAME} ЗАПУЩЕН ---")
    logger.info(f"Режим: {settings.ENVIRONMENT.upper()}")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Модуль интеграции с MES",
    version="1.0.0",
    lifespan=lifespan,
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)  # ✅ единственный правильный вариант

    process_time = time.perf_counter() - start_time

    logger.info(f"Запрос {request.url.path} обработан за {process_time:.4f} сек")

    response.headers["X-Process-Time"] = str(process_time)

    return response

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "alive", "service": settings.PROJECT_NAME}

if __name__ == "__main__":
    print(f"Запуск {settings.PROJECT_NAME} на http://{settings.APP_HOST}:{settings.APP_PORT}")
    uvicorn.run(
        "src.cli:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
    )
