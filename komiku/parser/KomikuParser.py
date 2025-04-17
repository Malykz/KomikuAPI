from parsel import Selector
import requests
import httpx
class KomikuParser :
    host = "komiku.id"
    userAgent = "Mozilla"
    headers = {
        "user-agent" : "Mozilla"
    }
    is_async = False

    async def asyn(self, client: httpx.AsyncClient) :
        self.page = await self.as_render_page(self.url, client=client)
        self.is_async = True
        return self

    def route_to_url(self, route:str, slash=False) -> str :
        if slash :
            return "https://" + self.host + "/" + route
        return "https://" + self.host + route

    def render_page(self, url:str) -> Selector:
        page = requests.get(url, headers=self.headers)
        return Selector(
            page.text if page.status_code == 200 else self.end(page.status_code)
        )

    # Deprecated
    def _send_request(self, url) :
        page = requests.get(url, headers=self.headers)
        return page.text, page.status_code

    async def as_render_page(self, url:str, client: httpx.AsyncClient) -> Selector:
        page = await client.get(url, headers=self.headers, follow_redirects=True)
        return Selector(
            page.text if page.status_code == 200 else self.end(page.status_code)
        )
    
    # Deprecated
    def sort_it(self, sentance) :
        try : return [int(word) for word in sentance.split(" ") if word.isdigit()][0]
        except : return sentance
    
    def get_slug(self, url) :
        if "/manga/" in url : 
            slug = url[ url.index("/manga/") + 7 : ]
        else :
            slug = url
        return slug.replace("/","")
