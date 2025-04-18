from parsel import Selector
import requests
import httpx
import asyncio
from user_agent import generate_navigator
class KomikuParser :
    host = "komiku.id"
    userAgent = "Mozilla"
    headers = generate_navigator()
    is_async = False

    async def asyn(self, client: httpx.AsyncClient) :
        self.page = await self.as_render_page(self.url, client=client)
        self.is_async = True
        return self

    def route_to_url(self, route: str, slash: bool = False) -> str:
        separator = "/" if slash else ""
        return f"https://{self.host}{separator}{route}"


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
    
    def get_slug(self, url: str) -> str:
        prefix = "/manga/"
        slug = url.split(prefix, 1)[-1] if prefix in url else url
        return slug.replace("/", "")
