import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend

from Models.Request import Request
async def repo_Details_Handler(username,reponame):

    req = Request(f"https://api.github.com/repos/{username}/{reponame}")
    response,statusCode = await req._api_call()
    if(statusCode==200):
        JsonData = {}
        JsonData['Name'] = response['name']
        JsonData['Description'] = response['description']
        JsonData['Star Count'] = response['stargazers_count']
        JsonData['Fork Count'] = response['forks_count']
        JsonData['Language'] = response['language']
        print(JsonData)
        return JsonData,statusCode
    else:
        return response,statusCode



    # print("ENTERED ",username,time.ctime())
    
    async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
        url1 = f"https://api.github.com/repos/{username}/{reponame}"
        async with session.get(url1) as response1:
            Data = await response1.json()
            if(response1.status==200):
                # print(Data)
                JsonData['Name'] = Data['name']
                JsonData['Description'] = Data['description']
                JsonData['Star Count'] = Data['stargazers_count']
                JsonData['Fork Count'] = Data['forks_count']
                JsonData['Language'] = Data['language']
                JsonData['Status Code'] = "200"
                return JsonData
            elif(response1.status == 404):
                return {"Message":Data['message'],"Status Code":"404"}
            else:
                return{"Message":"Server Error","Status Code":"500"}

    

        


                

    









    

    