from .KomikuParser import KomikuParser

class MangaParser(KomikuParser) :
    def __init__(
        self,
        slug = None,
    ) :
        self.url = f"https://{self.host}/manga/{slug}"
        self.page = self.render_page(self.url)

    @property
    def chapters_url(self) -> dict:
        result = []
        for el in self.page.css("table#Daftar_Chapter tbody tr td a") :
            print(el.css("a::attr(href)").get())
            result.append(
                {
                    "chapter" : el.css("a span::text").get(),
                    "url" : self.route_to_url(el.css("a::attr(href)").get()),
                    "slug" : self.get_slug(el.css("a::attr(href)").get())
                }
            )
        return result            
    
    @property
    def result(self) -> dict :
        raw_data = self.page.css("table.inftable tr td::text")
        poster = self.page.css("section#Informasi div.ims img::attr(src)").get()

        result = {
            "title" : raw_data[1].get(),
            "judul" : raw_data[3].get(),
            "poster" : poster[ : poster.index("?") ],
            "author" : raw_data[8].get(),
            "totalChapters" : len(self.chapters_url),
            "chapters" : self.chapters_url
        }
        return result
