from .KomikuParser import KomikuParser
from urllib.parse import urlparse

class SearchPageParser(KomikuParser) :
    _order_by = {
        "rank" : "meta_value_num",
        "new" : "date",
        "rand" : "rand"
    }
    _order_type = ["manga", "manhua", "manhwa"]

    
    def __init__(self, judul = None):
        self.judul = judul
        self.url = f"https://api.komiku.id/?post_type=manga&s={self.judul}"
        self.page = self.render_page(self.url)

    @property
    def result(self) :
        data = self.page.css("div.bge")
        result = [{} for i in data]

        i = 0
        for raw_data in data :
            img = raw_data.css("a img::attr(src)").get()
            result[i]["img"] = img[: img.index("?")]
            result[i]["url"] = f"https://{self.host}{raw_data.css("a::attr(href)").get()}"
            result[i]["slug"] = self.get_slug(raw_data.css("a::attr(href)").get())
            result[i]["title"] = raw_data.css("div.kan a h3::text").get().strip()
            result[i]["titleId"] = raw_data.css("span.judul2::text").get()
            result[i]["detail"] = raw_data.css("p::text").get().strip()

            i += 1

        return result
    
    def top(self, orderby, type) :
        if orderby not in self._order_by.keys() : raise Exception("Invalid Sort")
        if type not in self._order_type : raise Exception("Invalid Type")

        base_url = f"https://api.komiku.id/other/hot/?orderby={orderby}&category_name={type}"
        page = self.render_page(base_url)

        data = page.css("div.bge")
        result = [{} for i in data]

        i = 0
        for raw_data in data :
            img = raw_data.css("a img::attr(src)").get()
            result[i]["img"] = img[: img.index("?")]
            result[i]["url"] = raw_data.css("a::attr(href)").get()
            result[i]["slug"] = self.get_slug(raw_data.css("a::attr(href)").get())
            result[i]["title"] = raw_data.css("div.kan a h3::text").get().strip()
            result[i]["views"] = raw_data.css("span.judul2::text").get()
            result[i]["detail"] = raw_data.css("p::text").get().strip()

            i += 1

        return result