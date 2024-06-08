from fastapi import Depends, FastAPI
# from .schemas import db_models as models
from dotenv import load_dotenv

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from fastapi import Depends, FastAPI

from .routers import plagiary_search, sync_ingestion, metadata, async_ingestion

app = FastAPI(title="vectorStoreAPI")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    router=sync_ingestion.router,
    prefix="/sync/ingestion",
    tags=["Video uploading"]
)

app.include_router(
    router=async_ingestion.router,
    prefix="/async/ingestion",
    tags=["Video uploading"]
)

app.include_router(
    router=plagiary_search.router,
    prefix="/sync/plagiary",
    tags=["Plagiary search"]
)

app.include_router(
    router=metadata.router,
    prefix="/metadata/video",
    tags=["Metadata retrieving"]
)


@app.get("/")
async def health_check():
    return {"message": "Service is alive"}