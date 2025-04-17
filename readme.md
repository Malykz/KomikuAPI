# KomikuAPI
## About
Unofficial Komiku.id API. Writen in Python with Asynchronus Support. The way it works is by sending a request to Komiku.id and parsing the response from HTML to JSON.

## Quick Start
### Embed (Python)
```bash
pip install git+https://github.com/Malykz/KomikuAPI
```
```python
import komiku

ruri: dict = komiku.Manga("ruri-dragon").result
ruri["title"] # Ruri Dragon
```
### Cloning Repo 
```bash
git clone https://github.com/Malykz/KomikuAPI
cd KomikuAPI
pip install -r req.txt
uvicorn test:app
```

## End Points
| endpoint | method | query | decs |
|---|---|---|---|
| manga/{slug} | GET | - | Get metadata from a manga |
|chapter/{slug}| GET | - | Get chapter metadata from a manga |
|search | GET | q | Search Manga(s) |
|search/top| GET | orderby, type | Get trending manga info |