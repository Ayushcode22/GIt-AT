from sanic import Sanic, Blueprint
from sanic.response import text,json
from sanic_ext import render
import sys
from Managers.RouteHandlers.repoComparison import repoComparisonHandler
from Managers.RouteHandlers.userComparison import userComparisonHandler
sys.path.append('/Users/ayush.tripude/Desktop/Github Analytics tool')

from Managers.User import User
from Managers.Repository import Repository

bp = Blueprint("Ayush")


@bp.get('/')
async def hello(request):
    return text("Hello Ayush")



#CREATE HELP MENU
@bp.get('/help')
async def get_help(request):
    List = [
        " Use route '/user/<username>' to fetch user details ",
        " Use route '/user/<username><reponame>' to fetch details pf particular repository ",
        " Use route '/user/<username>/repos' to fetch names of all repositories of that user ",
        " Use route '/user/<username>/sort?type=<sort_type> for sorting all repositories pf that user ",
        " Use route '/user_comparison for comparing two users. Pass user1 and user2 as query parameters'. ",
        " Use route '/repo_compare' for comparing repositories. Pass user1,repo1,user2,repo2 in request body "
        ]
    return await render(
        "help.html",context = {"Menu":List} ,status=200
    )



# GET USER DETAILS
@bp.get('/user/<username:str>')
async def get_user_details(request,username):
    user = User(username)
    response, statusCode = await user.userDetailsHandler()
    if(statusCode==200):
        return await render('dummy_user_detail.html',context={"dict":response},status=200)
    else:
        return json(response)



#GET REPOSITORY DETAILS FOR A PARTICULAR USER
@bp.get('/user/<username:str>/<reponame:str>')
async def get_repo_details(request,username,reponame):
    repo = Repository(username,reponame)
    response,statusCode =  await repo.repoDetailsHandler()
    if(statusCode==200):
        return await render ('dummy_repo_details.html',context={"dict":response},status=200)
    else:
        return json(response)


#GET ALL REPOSITORIES FOR A USER
@bp.get('/user/<username:str>/repos')
async def get_user_repos(request,username):
    user = User(username)
    response = await user.repo_List_Handler()
    return await render("dummy_repo_list.html",context={"names":response},status=200)


@bp.get('/user/<username:str>/sort')
async def sort_Repos(request,username):
    user = User(username)
    response,statusCode = await user.handle_sorting(request)
    if(statusCode==200):
        return await render("dummy_sort.html",context={"List":response['List']},status=200)
    else:
        return json(response)


@bp.get('/user_comparison')
async def compare_user(request):
    response ,statusCode = await userComparisonHandler(request)
    if(statusCode==200):    
        return await render("dummy_table.html", context={"content1":response['user1'],"content2":response['user2']}, status=200)
    else:
        return json(response)


@bp.post('/repo_compare')
async def comapre_repos(request):
    response , statusCode = await repoComparisonHandler(request)
    if(statusCode==200):
        return await render(
            "dummy_repo_comp.html",context={"content1":response['repo1'],"content2":response['repo2']}, status=200
        ) 
    else:
        return json(response)