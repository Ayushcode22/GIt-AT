from Models.Request import Request
async def get_User_Lang(username):

    req = Request(f'https://api.github.com/users/{username}/repos')
    response,statusCode = await req._api_call()
    if(statusCode==200):
        JsonData={}
        languages = list(set([repo['language'] for repo in response if repo['language'] ]))
        JsonData['Languages'] = languages
        JsonData['Status Code'] = "200"
        return JsonData,statusCode
    else:
        return response,statusCode
