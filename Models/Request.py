import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend

class Request :
    def __init__(self,url):
        self.url = url
        # print(self.url)
    
    async def _api_call(self):
        print(self.url)
        async with CachedSession(cache=SQLiteBackend(cache_name='demo_cache',expire_after=60*60)) as session:
            url2 = self.url
            timeout = aiohttp.ClientTimeout(total=60*3)
            try:
                async with session.get(url2 , timeout=timeout) as response2:
                    data = await response2.json()
                    print(f"{response2.from_cache} Cache Used")
                    if(response2.status==200):
                        return data,response2.status
                    else:
                        data['documentation_url'] = 'http://127.0.0.1:8000/help'
                        return data,response2.status
            except aiohttp.ServerTimeoutError :
                return {"Message":"Server Timed Out"}, response2.status
