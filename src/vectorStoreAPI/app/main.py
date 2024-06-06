from fastapi import Depends, FastAPI
# from .schemas import db_models as models
from dotenv import load_dotenv

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="Orchestrator")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(
    router=items_retrieving.router,
    prefix="/items",
    tags=["Items retrieving"]
)


@app.get("/")
async def health_check():
    return {"message": "Service are Ivan and Vlad"}