from .KomikuParser import KomikuParser

class MangaParser(KomikuParser) :
    def __init__(
        self,
        slug = None,
        url = None,
    ) :
        self.url = url or f"https://{self.host}/manga/{slug}"
        self.page = self.render_page(self.url)

    @property
    def chapters_url(self) -> dict:
        result = {}
        for el in self.page.css("table#Daftar_Chapter tbody tr td a") :
            print(el.css("a::attr(href)").get())
            result.update(
                { self.sort_it(el.css("a span::text").get()) : self.route_to_url(el.css("a::attr(href)").get()) }
            )
        return result            
    
    @property
    def result(self) -> dict :
        raw_data = self.page.css("table.inftable tr td::text")
        result = {
            "title" : raw_data[1].get(),
            "judul" : raw_data[3].get(),
            "author" : raw_data[8].get(),
            "totalChapters" : len(self.chapters_url),
            "chapters" : self.chapters_url
        }
        return result
