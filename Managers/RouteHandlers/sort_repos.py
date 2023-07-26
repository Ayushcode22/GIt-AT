from aiohttp_client_cache import CachedSession, SQLiteBackend

from Models.Request import Request
from sanic.response import json


GIT_PATH = "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"

headers = {
        "AUTHENTICATION":f"Bearer{GIT_PATH}"
}


async def handle_sorting(request,username):

    
    try:
        query_params = request.args
        sort_type = query_params['type'][0]
    except:
        return {"Error Message ":" Please use 'type' as parameter of sorting"},404

    req = Request(f"https://api.github.com/users/{username}/repos")
    response1 ,statusCode1 = await req._api_call()

    if(statusCode1==200):
        Sorted_List=[]
        for repos in response1 :
            repo_name = repos['name']
            req2 = Request(f"https://api.github.com/repos/{username}/{repo_name}/contributors")
            response2 ,statusCode2 = await req2._api_call()
            if(statusCode2==200):
                for ctbtr in response2:
                    total_contribution = 0
                    total_contribution+=ctbtr['contributions']
                temp=[repos['forks_count'],repos['stargazers_count'],total_contribution,repo_name]
                Sorted_List.append(temp)
                match sort_type:
                    case 'fork':
                        Sorted_List.sort(key=lambda Sorted_List:Sorted_List[0])
                    case 'star':
                        Sorted_List.sort(key=lambda Sorted_List:Sorted_List[1])
                    case 'recent_activity':
                        Sorted_List.sort(key=lambda Sorted_List:Sorted_List[2])
                    case _ :
                        return {"Message":"Use 'fork' ,'star','recent_activity' as sorting parameters"},404
            else:
                return response2,statusCode2
        return {"List":Sorted_List},statusCode1
    else:
        return response1,statusCode1
        



    async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
        url1 = f"https://api.github.com/users/{username}/repos"
        async with session.get(url1,headers =headers) as response1:
            if(response1.status==200):
                total_contribution = 0
                Data = await response1.json()
                Sorted_List=[]
                for repos in Data :
                    repo_name = repos['name']
                    url2 = f"https://api.github.com/repos/{username}/{repo_name}/contributors"
                    async with session.get(url2) as response2:
                        if(response2.status==200):   
                            Contributors = await response2.json()
                            for ctbtr in Contributors:
                                total_contribution+=ctbtr['contributions']
                        temp=[repos['forks_count'],repos['stargazers_count'],total_contribution,repo_name]
                        Sorted_List.append(temp)
                        match sort_type:
                            case 'fork':
                                Sorted_List.sort(key=lambda Sorted_List:Sorted_List[0])
                            case 'star':
                                Sorted_List.sort(key=lambda Sorted_List:Sorted_List[1])
                            case 'recent_activity':
                                Sorted_List.sort(key=lambda Sorted_List:Sorted_List[2])
                            case _ :
                                return {"Message":"Use 'fork' ,'star','recent_activity' as sorting parameters","Status Code":"404"}
                return {"List":Sorted_List,"Status Code":"200"}

            else:
                return{"Message":"Server Error","Status Code":"500"}
    