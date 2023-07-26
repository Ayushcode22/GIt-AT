import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend

from Models.Request import Request


async def popular_repository(username):
    req = Request(f'https://api.github.com/users/{username}/repos')
    response,statusCode = await req._api_call()
    if(statusCode==200):
        popular_repos=[]
        JsonResponse={}
        for repo in response:
            popular_repos.append([repo['forks_count']+repo['stargazers_count'],repo['name']])
        popular_repos.sort(key=lambda popular_repos:popular_repos[0],reverse=True)
        JsonResponse['Popular Repos'] = popular_repos
        
        return JsonResponse,statusCode
    else:
        return response,statusCode