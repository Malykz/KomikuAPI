import requests
import json
from parsel import Selector

class KomikuParser :
    host = "komiku.id"
    userAgent = "Mozilla"
    headers = {
        "user-agent" : "Mozilla"
    }

    def render_page(self, url:str) -> Selector:
        page, code = self._send_request(url)
        sel = Selector(
            page if code == 200 else self.end(code)
        )
        return sel

    def route_to_url(self, route:str, slash=False) -> str :
        if slash :
            return "https://" + self.host + "/" + route
        return "https://" + self.host + route

    def _send_request(self, url) :
        print("Bruh. You Fucking Idiot")
        page = requests.get(url, headers=self.headers)
        return page.text, page.status_code

    def sort_it(self, sentance) :
        print(sentance)
        try : return [int(word) for word in sentance.split(" ") if word.isdigit()][0]
        except : return sentance
    
    def get_slug(self, url) :
        return url.replace("/manga/", "").replace("/","")

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

class MangaParser(KomikuParser) :
    def __init__(
        self,
        slug = None,
        url = None,
    ) :
        self.url = url or f"https://{self.host}/manga/{slug}"
        self.page = self.render_page(self.url)

    @property
    def chapters_url(self) -> None:
        result = {}
        for el in self.page.css("table#Daftar_Chapter tbody tr td a") :
            print(el.css("a::attr(href)").get())
            result.update(
                { self.sort_it(el.css("a span::text").get()) : self.route_to_url(el.css("a::attr(href)").get()) }
            )
        return result            
    
    @property
    def result(self) :
        raw_data = self.page.css("table.inftable tr td::text")
        result = {
            "title" : raw_data[1].get(),
            "judul" : raw_data[3].get(),
            "author" : raw_data[8].get(),
            "totalChapters" : len(self.chapters_url),
            "chapters" : self.chapters_url
        }
        return result


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
    

prop = ChapterParser(url="https://komiku.id/kaguya-sama-wa-kokurasetai-official-dj-chapter-20-bahasa-indonesia/").result
breakpoint()
