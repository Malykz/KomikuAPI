import komiku
from fastapi import FastAPI

app = FastAPI()

@app.get("/search")
def read_root(search:str):
    return komiku.Search(search).result

@app.get("/manga/{slug}")
def read_root(slug:str):
    return komiku.Manga(slug).result

@app.get("/chapter/{slug}")
def get_chapter(slug:str):
    return komiku.Chapter(slug).result

@app.get("/top/")
def re(type:str = "manga", sort:str = "new"):
    return komiku.Search().top(sort, type)