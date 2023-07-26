from Models.Request import Request
import asyncio

class Repository:

    def __init__(self,username,reponame):
        self.user = username
        self.repo = reponame

    async def repo_Details_Handler(self):
        req = Request(f"https://api.github.com/repos/{self.user}/{self.repo}")
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
        

    async def repoDetailsHandler(self):
        task1 = asyncio.get_event_loop().create_task(self.repo_Details_Handler())
        task2 = asyncio.get_event_loop().create_task(self.repoContributorsHandler())
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

    async def repoContributorsHandler(self):
        req = Request(f"https://api.github.com/repos/{self.user}/{self.repo}/contributors")
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