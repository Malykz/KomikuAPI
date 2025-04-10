from .KomikuParser import KomikuParser
import json

class ChapterParser(KomikuParser) :
    def __init__(
        self,
        url,
    ) :
        self.url = url
        self.page = self.render_page(url)

    def end(self, code) : 
        raise Exception(f"Failed to send request, Http Code : {code}")
    
    @property
    def result(self) :
        result = {}
        addictional_data = json.loads(self.page.css('script[type="application/ld+json"]::text')[1].get().strip())
        result.update(addictional_data)
        
        result["totalPage"] = self.page.css("span.chapterInfo::attr(valuechapter)").get().replace(" ", "-")
        result["pagesUrl"] = [mangaImageUrl for mangaImageUrl in self.page.css("div#Baca_Komik img::attr(src)").getall()]
        result["slug"] = self.page.css("span.chapterInfo::attr(valuelink)").get().replace("/","")
        
        return result