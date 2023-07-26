import aiohttp
import asyncio
from sanic.response import json
from Managers.get_popular_repository import popular_repository
from Managers.user_details import user_Details
from Models.Response import Response

async def userDetailsHandler(username):
    print("Entered Handler")
    task1 = asyncio.get_event_loop().create_task(user_Details(username))
    task2 = asyncio.get_event_loop().create_task(popular_repository(username))
    group = await asyncio.gather(*[task1,task2],return_exceptions=True)

    # respo1 = Response(group[0][0])
    print(group)
    respo1 = group[0][0]
    respo2 = group[1][0]
    # respo2 = Response(group[1][0])
    status1 = group[0][1]
    status2 = group[1][1]
    if(status1==200 and status2==200):
        popular_repos = []
        for i,repo in enumerate(respo2['Popular Repos']):
            if(i>1):
                break
            else:
                popular_repos.append(repo[1])
        
        respo1['Popular Respositories'] = popular_repos
        # finalResponse = Response(group[0][0])
        # print(finalResponse.data)
        return respo1,status1

    elif(status1!=200):
        return respo1,status1
    else:
        return respo2,status2