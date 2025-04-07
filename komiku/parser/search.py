from .KomikuParser import KomikuParser

class SearchPageParser(KomikuParser) :
    def __init__(self,judul):
        self.judul = judul
        self.url = f"https://api.komiku.id/?post_type=manga&s={self.judul}"
        self.page = self.render_page(self.url)

    @property
    def result(self) :
        data = self.page.css("div.bge")
        result = [{} for i in data]

        i = 0
        for raw_data in data :
            result[i]["url"] = f"https://{self.host}{raw_data.css("a::attr(href)").get()}"
            result[i]["slug"] = self.get_slug(raw_data.css("a::attr(href)").get())
            result[i]["title"] = raw_data.css("div.kan a h3::text").get().strip()
            result[i]["titleId"] = raw_data.css("span.judul2::text").get()
            result[i]["detail"] = raw_data.css("p::text").get().strip()

            i += 1

        return result