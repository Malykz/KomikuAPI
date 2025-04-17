from parsel import Selector
import requests
import httpx
import asyncio
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
        self.response = page.status_code
        return Selector(
            page.text if page.status_code == 200 else self.end(page.status_code)
        )

    async def _set_asyn_result(self) :
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._set_result)

    @property
    def result(self) :
        self.t_result = {
            False : self._set_result,
            True : self._set_asyn_result
        }.get(self.is_async)
        
        return self.t_result()

    async def as_render_page(self, url:str, client: httpx.AsyncClient) -> Selector:
        page = await client.get(url, headers=self.headers, follow_redirects=True)
        self.response = page.status_code
        return Selector(
            page.text if page.status_code == 200 else self.end(page.status_code)
        )
    
    def get_slug(self, url) :
        if "/manga/" in url : 
            slug = url[ url.index("/manga/") + 7 : ]
        else :
            slug = url
        return slug.replace("/","")
