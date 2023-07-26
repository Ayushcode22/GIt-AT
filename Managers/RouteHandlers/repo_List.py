from aiohttp_client_cache import CachedSession, SQLiteBackend
from Models.Request import Request

async def repo_List_Handler(username):
    req = Request(f'https://api.github.com/users/{username}/repos')
    response , statusCode = await req._api_call()
    if(statusCode==200):
        names ={}
        for i,obj in enumerate(response):
            names[f'Repos {i+1}']= obj['name']
        return names