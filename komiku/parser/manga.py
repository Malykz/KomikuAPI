from .KomikuParser import KomikuParser
import asyncio
class MangaParser(KomikuParser) :
    def __init__(
        self,
        slug = None,
    ) :
        self.url = f"https://{self.host}/manga/{slug}"

    def end(self, code) :
        raise Exception(f"Error rendering with Httpcode : {code}")

    @property
    def chapters_url(self) -> dict:
        result = []
        for el in self.page.css("table#Daftar_Chapter tbody tr")[1:] :
            chapter = el.css("td.judulseries a span::text").get()
            release = el.css("td.tanggalseries::text").get().strip()

            url  = self.route_to_url(el.css("a::attr(href)").get())
            slug = self.get_slug(el.css("a::attr(href)").get())

            result.append(
                {
                    "chapter" : chapter,
                    "release" : release,
                    "url" : url,
                    "slug" : slug
                }
            )
        return result            
    
    def __validation(self) -> None :
        if self._is_async is not True :
            self.page = self.render_page(self.url)

    def _set_result(self) -> dict :
        if self.page == None : return None  

        raw_data = self.page.css("table.inftable tr td::text")
        title    = raw_data[1].get()
        judul    = raw_data[3].get()
        author   = raw_data[8].get()
        status   = raw_data[10].get()
        
        poster   = self.page.css("section#Informasi div.ims img::attr(src)").get()
        poster   = poster[ : poster.index("?") ]

        sinopsis = self.page.css("p.desc::text").get().strip()
        genre    = self.page.css("ul.genre li a span::text").getall()

        chapters = self.chapters_url
        totalchapter = len(chapters)



        result = {
            "title" : title,
            "judul" : judul,
            "genre" : genre,
            "status" : status,
            "sinopsis" : sinopsis, 
            "poster" : poster,
            "author" : author,
            "totalChapters" : totalchapter,
            "chapters" : chapters
        }

        return result
