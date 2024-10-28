from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from loguru import logger

from src.api import router as api_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    logger.success('App is started up')
    yield
    logger.error('App is shutting down...')


app = FastAPI(title='Market API', lifespan=lifespan)

app.include_router(api_router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('app:app', host='localhost', port=8080, reload=True)
