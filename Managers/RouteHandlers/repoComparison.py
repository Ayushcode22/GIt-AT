import asyncio
from ..Repository import Repository
async def repoComparisonHandler(request):
    
    try:
        body = request.json
        user1 =body['user1']
        user2 = body['user2']
        repo1 = body['repo1']
        repo2 = body['repo2']
    except:
        return {"Error Message ":" Please use 'user1' and 'user2' for passing username and 'repo1' and 'repo2' for passing repository name"},404
    
    repo1 = Repository(user1,repo1)
    repoDetails1 = asyncio.get_event_loop().create_task( repo1.repoDetailsHandler())
    repo2 = Repository(user2,repo2)
    repoDetails2 = asyncio.get_event_loop().create_task(repo2.repoDetailsHandler())

    group = await asyncio.gather(*[repoDetails1,repoDetails2],return_exceptions=True)
    print(group)

    resp1 = group[0][0]
    resp2 = group[1][0]

    statusCode1 = group[0][1]
    statusCode2 = group[1][1]

    if(statusCode1==200 and statusCode2==200):
        resp1['username1'] = user1
        resp2['username2'] = user2
        FinalResponse = {}
        FinalResponse['repo1'] = resp1
        FinalResponse['repo2'] = resp2
        return FinalResponse,200
    elif(statusCode2!=200):
        return resp2,statusCode2
    else:
        return resp1,statusCode1




