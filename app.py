from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from loguru import logger

from src.api import router as api_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    logger.success('App is started up')
    yield
    logger.error('App is shutting down...')


app = FastAPI(
    title='Market API',
    lifespan=lifespan
)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT'],
    allow_headers=['*']
)

app.include_router(api_router, prefix='/api', tags=['API'])


if __name__ == '__main__':
    uvicorn.run('app:app', host='localhost', port=8080, reload=True)
