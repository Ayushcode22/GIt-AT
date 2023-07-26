import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend

from Models.Request import Request

async def mostStarredRepoHandler(username):
    req = Request(f'https://api.github.com/users/{username}/repos')
    response,statusCode = await req._api_call()
    if(statusCode==200):
        JsonData={}
        max_star =0
        mostStarRepo =''
        repo_link = ''
        for repo in response:
            star = repo['stargazers_count']
            if(star>max_star):
                mostStarRepo = repo['name']
                repo_link = repo['html_url']
                max_star = star
        temp = {}
        temp['Repo Name'] = mostStarRepo
        temp['Number of Stars'] = max_star
        temp['Repository Link'] = repo_link
        JsonData['Most Starred Repo'] =temp
        return JsonData,statusCode
    else:
        response,statusCode







    # async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
    #     url = f'https://api.github.com/users/{username}/repos'
    #     async with session.get(url) as response:
    #         data = await response.json()
            
    #         if(response.status==200):
    #             for repo in data:
    #                 star = repo['stargazers_count']
    #                 if(star>max_star):
    #                     mostStarRepo = repo['name']
    #                     repo_link = repo['html_url']
    #                     max_star = star
    #             temp = {}
    #             temp['Repo Name'] = mostStarRepo
    #             temp['Number of Stars'] = max_star
    #             temp['Repository Link'] = repo_link
    #             JsonData['Most Starred Repo'] =temp
    #             JsonData['Status Code'] = "200"
    #             return JsonData
    #         else:
    #             return {
    #                 "Message":"Error 404","Status Code":"404"
    #             }