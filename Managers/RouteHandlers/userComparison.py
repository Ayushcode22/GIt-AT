import asyncio
from ..User import User


async def userComparisonHandler(request):
    try:
        query_params = request.args
        user1 = query_params['user1'][0]
        user2 = query_params['user2'][0]
    except:
        return {"Error Message ":" Please use 'user1' and 'user2' for passing username"},404

    user1 = User(user1)
    response1 =asyncio.get_event_loop().create_task( user1.userDetailsHandler())
    user2 = User(user2)
    response2 =asyncio.get_event_loop().create_task( user2.userDetailsHandler())
    

    user_1_mostStarred = asyncio.get_event_loop().create_task(user1.mostStarredRepoHandler()) 
    user_2_mostStarred = asyncio.get_event_loop().create_task(user2.mostStarredRepoHandler())

    lang_u1 = asyncio.get_event_loop().create_task(user1.get_User_Lang())
    lang_u2 = asyncio.get_event_loop().create_task(user2.get_User_Lang())

    group = await asyncio.gather(*[response1,response2,user_1_mostStarred,user_2_mostStarred,lang_u1,lang_u2],return_exceptions=True)
    
    print(group)
    
    resp1 = group[0][0]
    resp2 = group[1][0]
    resp3 = group[2][0]
    resp4 = group[3][0]
    resp5 = group[4][0]
    resp6 = group[5][0]


    status1 = group[0][1]
    status2 = group[1][1]
    status3 = group[2][1]
    status4 = group[3][1]
    status5 = group[4][1]
    status6 = group[5][1]

    if(status1==200 and status2==200 and status3==200 and status4==200 and status5==200 and status6==200):

        resp1['Most Starred Repo'] = resp3['Most Starred Repo']
        resp2['Most Starred Repo'] = resp4['Most Starred Repo']
        resp1['Languages'] = resp5['Languages']
        resp2['Languages'] = resp6['Languages']
        JsonResp ={}
        JsonResp['user1']=resp1
        JsonResp['user2']=resp2
        return JsonResp,status1
    elif(status1!= 200):
        return resp1,status1
    elif(status2!= 200):
        return resp2,status2
    elif(status3!= 200):
        return resp3,status3
    elif(status4!= 200):
        return resp4,status4
    elif(status5!= 200):
        return resp5,status5
    else :
        return resp6,status6
