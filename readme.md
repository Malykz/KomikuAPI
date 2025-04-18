# KomikuAPI
## About
Unofficial Komiku.id API. Writen in Python with Asynchronus Support. The way it works is by sending a request to Komiku.id and parsing the response from HTML to JSON.
<br><br>5790+ manga and 309400+ chapters available

## Quick Start
### Embed (Python)
```bash
pip install git+https://github.com/Malykz/KomikuAPI
```
<br><b>Synchronous</b>
```python
import komiku

resp = komiku.Manga("ruri-dragon") # Send Request
ruri = resp.result # Parse the Response
ruri["title"] # "Ruri Dragon"
```
<br><b>Asynchronous</b>
```python
import komiku
import httpx

async with httpx.AsyncClient() as client :
    resp = await komiku.Manga("ruri-dragon").asyn(client) # Send Request
    ruri = await resp.result # Parse the Response
    ruri["title"] # "Ruri Dragon"
```
### Rest API
```bash
git clone https://github.com/Malykz/KomikuAPI
cd KomikuAPI
pip install -r req.txt
uvicorn server:app
```
```bash
curl -X GET http://localhost:8000/manga/ruri-dragon
```

## End Points
| endpoint | method | query | decs |
|---|---|---|---|
| manga/{slug} | GET | - | Get metadata from a manga |
|chapter/{slug}| GET | - | Get chapter metadata from a manga |
|search | GET | q | Search Manga(s) |
|search/top| GET | orderby, type | Get trending manga info |

## Classes
There are 3 main classes : `Manga`, `Chapter`, `Search`. Each of which is a inheritance of the `KomikuParser` class.
### KomikuParser
A parent class that has classmethods for parsing common data, sending requests, and rendering the response.

<b>Method</b>
<ul>
    <li><code>render_page / as_render_page</code> method is designed to fetch and process the content of a web page from a given URL.</li>
    <li><code>async</code> is an asynchronous function that prepares the KomikuParser instance for asynchronous operations. It takes a single parameter, client, which is an instance of <code>httpx.AsyncClient</code></li>
    <li><code>get_slug</code> method is a utility function designed to extract a "slug" from a given URL. A slug is typically a unique identifier or part of a URL that represents a specific resource, such as a manga title in this case.</li>        
</ul>

<b>Disclaimer</b>
If you want to configure User-Agent and Navigator. But it's better not to need to reconfigure. The navigator is already set up that way.
```python
komiku.KomikuParser.headers = {"user-agent" : "python-httpx"}
```
### Manga
The class that handles parsing responses for all `/manga/` endpoints. Requires slug as primary parameter.

<b>Ex : Embed</b>
```python
ruri: dict = komiku.Manga("ruri-dragon").result
```
<b>Ex : Rest API</b>
```bash
curl -X GET http://localhost:8000/manga/ruri-dragon
```
<b><br>Output (Preview) :</b>
```json
{
  "title": "Ruri Dragon",
  "judul": "Ruri Si Naga",
  "genre": [
    "Comedy",
    "Fantasy",
    "Shounen",
    "Slice of Life"
  ],
  "status": "Ongoing",
  "sinopsis": "Kisah seorang gadis naga muda menjadi malas, melakukan yang terbaik ...",
  "poster": "https://cover.komiku.id/wp-content/uploads/2022/09/Manga-Ruri-Dragon.jpg",
  "author": "Shindou Masaoki",
  "totalChapters": 33,
  "chapters": [
    {
      "chapter": "Chapter 32",
      "release": "07/04/2025",
      "url": "https://komiku.id/ruri-dragon-chapter-32-2/",
      "slug": "ruri-dragon-chapter-32-2"
    },
    . . .
  ]
}  
```
### Chapter
The class that handles parsing responses for all `/chapter/` endpoints. Requires slug as primary parameter.

<b>Ex : Embed</b>
```python
ruri: dict = komiku.Search("ruri-dragon-chapter-32-2").result
```
<b>Ex : Rest API</b>
```bash
curl -X GET http://localhost:8000/chapter/ruri-dragon-chapter-32-2
```
<b><br>Output (Preview) :</b>
```json
{
  "id": "https://komiku.id/ruri-dragon-chapter-32-2/#main",
  "url": "https://komiku.id/ruri-dragon-chapter-32-2/",
  "name": "Komik Ruri Dragon Chapter 32",
  "headline": "Komik Ruri Dragon Chapter 32",
  "description": "Komik Ruri Dragon Chapter 32 bahasa Indonesia bahasa Indonesia bisa kamu baca di Komiku dengan kualitas gambar terbaik.",
  "keywords": "Ruri Dragon Chapter 32, Komik, Chapter, Bahasa, Indonesia, Indo, Baca",
  "thumbnail": "https://img.komiku.id/uploads4/2918826-11.jpg",
  "totalPage": "32",
  "pagesUrl": [
    "https://cdn.komiku.id/uploads4/2918826-1.jpg",
    "https://cdn.komiku.id/uploads4/2918826-2.jpg",
    . . .
  ]  
}  
```
### Search
The class that handles parsing responses for all `/top/` and `/search/` endpoints. Requires slug as parameter.

> Searching Manga with title

<br><b>Ex : Embed</b>
```python
ruri: list[dict] = komiku.Search("ruri").result
```
<b>Ex : Rest API</b>
```python
curl -X GET http://localhost:8000/search?q=ruri
```
<b><br>Output (Preview)</b>
```json
[
  {
    "img": "https://cover.komiku.id/wp-content/uploads/2022/09/Komik-Ruri-Dragon.jpg",
    "url": "https://komiku.id/manga/ruri-dragon/",
    "slug": "ruri-dragon",
    "title": "Ruri Dragon",
    "titleId": "Ruri Si Naga",
    "detail": "Update 1 minggu lalu. Kisah seorang gadis naga muda menjadi malas, melakukan yang terbaik ..."
  },
  . . .
]  
```
<br>

> Looking for trending manga

<br><b>Ex : Embed</b>
```python
ruri: list[dict] = komiku.Search("ruri").top("new", "manhua")
```
<b>Ex : Rest API</b>
```python
curl -X GET http://localhost:8000/top?sort=new&type=manhua
```
<b><br>Output (Preview)</b>
```json
[
  {
    "thumbnail": "https://cover.komiku.id/wp-content/uploads/2025/04/A1-I-Was-Forced-by-the-System-to-Become-a-Villain.jpg",
    "poster": "https://cover.komiku.id/wp-content/uploads/2025/04/A2-I-Was-Forced-by-the-System-to-Become-a-Villain.jpg",
    "url": "https://komiku.id/manga/i-was-forced-by-the-system-to-become-a-villain/",
    "slug": "i-was-forced-by-the-system-to-become-a-villain",
    "title": "I Was Forced by the System to Become a Villain",
    "views": "189rb x • 3 hari • Berwarna",
    "detail": "Lin Bei, yang melakukan perjalanan melintasi waktu dan menjadi saudara senior kedua dari Puncak Lingxi dari Sekte Qingyun,~"
  },
  . . .
]  
```