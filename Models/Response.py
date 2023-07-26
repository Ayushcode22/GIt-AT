from sanic.response import text,json
from sanic_ext import render


class Response:

    def __init__(self,data):
        self.data = data
        # print(data)

    async def renderJson(self,html_file,status_code):
        print(status_code)
        if(status_code==200):
            return await render(
                html_file,context={"dict":self.data},status=200
            ) 
        else:
            return json(self.data)
        
    # def check_status(self):
    #     d = self.data
    #     if d['Status Code']==200:
    #         return True
    #     else:
    #         return False