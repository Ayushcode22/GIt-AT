import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend

from Models.Request import Request
async def repoContributorsHandler(username,reponame):
    
    req = Request(f"https://api.github.com/repos/{username}/{reponame}/contributors")
    response ,statusCode = await req._api_call()
    if(statusCode==200):
        List_contributors=[]
        JsonResponse = {}
        for contrib in response:
            temp={}
            temp[contrib['login']] = contrib['contributions']
            List_contributors.append(temp)
        JsonResponse['List_contributors'] = List_contributors
        return JsonResponse,statusCode
    else:
        return response,statusCode