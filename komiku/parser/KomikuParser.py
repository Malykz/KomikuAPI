from parsel import Selector
import requests
import httpx
import asyncio
from user_agent import generate_navigator
from komiku.exception import *

class KomikuParser :
    host = "komiku.org"
    userAgent = "Mozilla"
    headers = generate_navigator()
    timeout = 5

    _is_async = False

    def syn(self) :
        self.page = self.render_page(self.url)
        self._is_async = False
        return self

    async def asyn(self, client: httpx.AsyncClient) :
        if type(client) == httpx.AsyncClient:
            self.page = await self.as_render_page(self.url, client=client)
            self._is_async = True
            return self
        
        else :
            raise InvalidClient(
                f"expecting client to have <class 'httpx.AsyncClient'> type, not {type(client)}"
            )

    def render_page(self, url:str) -> Selector:
        try:
            resp = requests.get(
                url,
                allow_redirects=True,
                timeout=self.timeout
            )

            self.code = resp.status_code
            self.is_success = resp.ok

            if not resp.ok :
                return None
            
            return Selector(resp.text)
        
        except Exception as e:
            raise Exception(e)            

        
    async def as_render_page(self, url:str, client: httpx.AsyncClient) -> Selector:
        try:
            resp = await client.get(
                url, 
                follow_redirects=True, 
                timeout=self.timeout
            )

            self.code = resp.status_code
            self.is_success = resp.is_success

            if not resp.is_success:
                return None

            return Selector(resp.text)

        except httpx.ConnectTimeout:
            raise YourInternetIsSucks(
                f"Failed to receive response within specified time: {self.timeout}"
            )
        
    async def _set_asyn_result(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._set_result)

    @property
    def result(self) :
        self.t_result = {
            False : self._set_result,
            True : self._set_asyn_result
        }.get(self._is_async)
        
        return self.t_result()


    def get_slug(self, url: str) -> str:
        prefix = "/manga/"
        slug = url.split(prefix, 1)[-1] if prefix in url else url
        return slug.replace("/", "")
    
    def route_to_url(self, route: str, slash: bool = False) -> str:
        separator = "/" if slash else ""
        return f"https://{self.host}{separator}{route}"
