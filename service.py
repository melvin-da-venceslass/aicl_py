from lib2to3.pytree import Base
from optparse import Option
from xmlrpc.client import Boolean
from fastapi import FastAPI,Request

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates



from typing import Optional
from pydantic import BaseModel
import pybase64
import time


#HTML LIBRARY
from fastapi.responses import HTMLResponse  #to render the ouput in HTML format text - html
from fastapi.staticfiles import StaticFiles #to access the files and folders that web app needs
from fastapi.templating import Jinja2Templates #  #to render the ouput in HTML format -  file to html




app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class CV(BaseModel):
   name:str
   age:int
   dev:bool
   hobby:Optional[list]

class EMPLOYEE(BaseModel):
    name:str
    exp:int
    yop:int
    age:int
    employeed:bool




@app.get("/hello/{my_query}")
def home(my_query, q:Optional[str]=None):
    return {"result":"sucess","user_input":my_query,"query":q}


@app.put("/endpoint")
async def endpoint( resume: CV):
    "some code db here"
    return {"username": resume.name}




@app.post("/mypostendpoint")
async def mpep(emp:EMPLOYEE):
    return {"emp":emp.name}


@app.get("/token")
async def tokenGenerator():

    timenow = bytes(str(time.time()),"utf-8")
    token = pybase64.b64encode(timenow, altchars='_:')
    with open("token.txt","a+") as tokenfile: 
        tokenfile.write(str(token) + "|\n" )
        tokenfile.close()
    return {"token":token}


@app.get("/mySecureEndpoint")
async def msep(token:str,field1:str, field2:str,):
    
    file = eval(str(open("token.txt","r+").readlines()))
    for each in file:
        if token in each:
             authorisation = "Welcome Home!"
             break
        else:
             authorisation = "Get Out!"
             pass
    
    return {"server_pass":authorisation}
     

@app.get("/webpage", response_class=HTMLResponse)
async def webpage():
    html_code = """
            <html>
            <head>
            </head>
            <body>
            <h1>Hello Folks
            </body>
            </html>
    
     """
    return html_code



class usr(BaseModel):
    name:str
    password:str
    email:str


@app.get("/login", response_class=HTMLResponse)
async def webpage(request:Request):
    return templates.TemplateResponse('index.html', context={'request': request})




@app.post("/create_user")
async def create_user(user:usr):

    userdb = eval(open("userdb.json","r").read())

    user_profile = {"name":user.name,
                    "password":user.password,
                    "email":user.email}

    userdb["users"].append(user_profile)
    open("userdb.json","w+").write(str(userdb))
    return {"status":"success"}

class usr_login(BaseModel):
    name:str
    password:str

@app.post("/login_user")
async def create_user(user:usr_login):
 

    userdb = eval(open("userdb.json","r").read())
    
    for each in  userdb["users"]:
        if each["name"]==user.name and each["password"]==user.password:
            return {"status":"Login Success"}
        else:
            pass
    return {"status":"Login Failure"}