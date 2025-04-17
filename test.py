import komiku
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import TypedDict, AsyncIterator
from starlette.applications import Starlette
from starlette.requests import Request
import contextlib
import httpx

class State(TypedDict):
    http_client: httpx.AsyncClient

@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[State]:
    async with httpx.AsyncClient() as client:
        yield {"http_client": client}

app = FastAPI(lifespan=lifespan)

@app.get("/search")
async def read_root(q:str, request: Request):
    result = await komiku.Search(q).asyn(request.state.http_client)
    respon = await result.result
    
    return respon

@app.get("/manga/{slug}")
async def read_root(slug:str, request: Request):
    result = await komiku.Manga(slug).asyn(request.state.http_client)
    respon = await result.result

    return respon

@app.get("/chapter/{slug}")
async def get_chapter(slug:str, request: Request):
    result = await komiku.Chapter(slug).asyn(request.state.http_client)
    respon = await result.result
    
    return respon

@app.get("/top/")
def re(type:str = "manga", sort:str = "new"):
    return komiku.Search().top(sort, type)