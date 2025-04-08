from parsel import Selector
import requests

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
