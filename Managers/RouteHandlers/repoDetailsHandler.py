import asyncio
from Managers.get_contributors import repoContributorsHandler

from Managers.repo_Details import repo_Details_Handler
from sanic.response import json



async def repoDetailsHandler(username,reponame):
    task1 = asyncio.get_event_loop().create_task(repo_Details_Handler(username,reponame))
    task2 = asyncio.get_event_loop().create_task(repoContributorsHandler(username,reponame))
    group = await asyncio.gather(*[task1,task2],return_exceptions=True)

    resp1 = group[0][0]
    resp2 = group[1][0]
    statusCode1 = group[0][1]
    statusCode2 = group[1][1]

    if(statusCode1==200 and statusCode2==200):
        resp1['List_contributors'] = resp2['List_contributors']
        return resp1,200

    elif(statusCode1!=200):
        return resp1,statusCode1
    else:
        return resp2,statusCode2