import komiku
from fastapi import FastAPI

app = FastAPI()

@app.get("/search/{search}")
def read_root(search:str):
    return komiku.Search(search).result


@app.get("/manga/{search}")
def read_root(search:str):
    return komiku.Manga(slug=search).result