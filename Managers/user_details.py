from aiohttp_client_cache import CachedSession, SQLiteBackend
from Models.Request import Request

GIT_PATH = "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"

headers = {
        "AUTHENTICATION":f"Bearer{GIT_PATH}"
    }

async def user_Details(username):
    req =  Request(f"https://api.github.com/users/{username}")
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
        print(response)
        return response,statusCode

    