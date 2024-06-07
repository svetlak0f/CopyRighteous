from fastapi import Depends, FastAPI
# from .schemas import db_models as models
from dotenv import load_dotenv

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from fastapi import Depends, FastAPI

from .routers import sync_ingestion

app = FastAPI(title="Orchestrator")

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
    tags=["Items retrieving"]
)


@app.get("/")
async def health_check():
    return {"message": "Service is alive"}