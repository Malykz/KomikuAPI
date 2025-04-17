from .KomikuParser import KomikuParser

class MangaParser(KomikuParser) :
    def __init__(
        self,
        slug = None,
    ) :
        self.url = f"https://{self.host}/manga/{slug}"
        self.page = self.render_page(self.url)

    def end(self, code) :
        raise Exception(f"Error rendering with Httpcode : {code}")

    @property
    def chapters_url(self) -> dict:
        result = []
        for el in self.page.css("table#Daftar_Chapter tbody tr")[1:] :
            result.append(
                {
                    "chapter" : el.css("td.judulseries a span::text").get(),
                    "release" : el.css("td.tanggalseries::text").get().strip(),
                    "url" : self.route_to_url(el.css("a::attr(href)").get()),
                    "slug" : self.get_slug(el.css("a::attr(href)").get())
                }
            )
        return result            
    
    def _set_result(self) -> dict :
        if self.is_async is not True : self.page = self.render_page(self.url)
        
        raw_data = self.page.css("table.inftable tr td::text")
        poster = self.page.css("section#Informasi div.ims img::attr(src)").get()
        sinopsis = self.page.css("p.desc::text").get().strip()
        genre = self.page.css("ul.genre li a span::text").getall()

        result = {
            "title" : raw_data[1].get(),
            "judul" : raw_data[3].get(),
            "genre" : genre,
            "status" : raw_data[10].get(),
            "sinopsis" : sinopsis, 
            "poster" : poster[ : poster.index("?") ],
            "author" : raw_data[8].get(),
            "totalChapters" : len(self.chapters_url),
            "chapters" : self.chapters_url
        }
        return result
