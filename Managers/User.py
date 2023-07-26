import asyncio
from Models.Request import Request

class User:

    def __init__(self,username):
        self.username = username
    

    async def repo_List_Handler(self):
        req = Request(f'https://api.github.com/users/{self.username}/repos')
        response , statusCode = await req._api_call()
        if(statusCode==200):
            names ={}
            for i,obj in enumerate(response):
                names[f'Repos {i+1}']= obj['name']
            return names



    async def userDetailsHandler(self):
        task1 = asyncio.get_event_loop().create_task(self.user_Details())
        task2 = asyncio.get_event_loop().create_task(self.popular_repository())
        group = await asyncio.gather(*[task1,task2],return_exceptions=True)
        
        respo1 = group[0][0]
        respo2 = group[1][0]
        
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
            return respo1,status1

        elif(status1!=200):
            return respo1,status1
        else:
            return respo2,status2
        

    async def get_User_Lang(self):
        req = Request(f'https://api.github.com/users/{self.username}/repos')
        response,statusCode = await req._api_call()
        if(statusCode==200):
            JsonData={}
            languages = list(set([repo['language'] for repo in response if repo['language'] ]))
            JsonData['Languages'] = languages
            JsonData['Status Code'] = "200"
            return JsonData,statusCode
        else:
            return response,statusCode
        
    async def popular_repository(self):
        req = Request(f'https://api.github.com/users/{self.username}/repos')
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
        
    async def mostStarredRepoHandler(self):
        req = Request(f'https://api.github.com/users/{self.username}/repos')
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

    async def user_Details(self):
        req =  Request(f"https://api.github.com/users/{self.username}")
        response,statusCode =  await req._api_call()
        if(statusCode==200):
            jsonData={}
            jsonData['Name'] = response['login']
            jsonData['Email'] = response['email']
            jsonData['Public Repos'] = response['public_repos']
            jsonData['Location'] = response['location']
            jsonData['Bio'] = response['bio']
            jsonData['User Type'] = response['type']
            jsonData['GitHub Profile Link'] = response['html_url']
            jsonData['Profile Picture Link'] = response['avatar_url']
            jsonData['Followers'] = response['followers']
            jsonData['Following'] = response['following']
            return jsonData,statusCode
        else:
            return response,statusCode    
        

    async def handle_sorting(self,request):
        try:
            query_params = request.args
            sort_type = query_params['type'][0]
        except:
            return {"Error Message ":" Please use 'type' as parameter of sorting"},404

        req = Request(f"https://api.github.com/users/{self.username}/repos")
        response1 ,statusCode1 = await req._api_call()

        if(statusCode1==200):
            Sorted_List=[]
            for repos in response1 :
                repo_name = repos['name']
                req2 = Request(f"https://api.github.com/repos/{self.username}/{repo_name}/contributors")
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