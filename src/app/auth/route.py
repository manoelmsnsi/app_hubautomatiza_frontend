from datetime import timedelta
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Form, HTTPException, Request,status

from src.app.home.route import home
from src.system.core.flash import get_flashed_messages
from src.system.integration.api_crm import ApiBackend





#CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG#
frontend = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
frontend.mount("/static", StaticFiles(directory="src/system/static", html=True), name="static")
templates = Jinja2Templates(directory=["src/app/auth/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/auth",)
async def auth_list(request: Request):
    try:
        data ={}# api_backend.get_auth(filters=request.query_params)
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"auth_list"},"error":error}})

@frontend.get("/auth/form",)
async def auth_form(request: Request):
    try:
        return templates.TemplateResponse("login.html",{"request": request})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"auth_form"},"error":error}})
@frontend.get("/auth/recuperar_senha",)
async def auth_form(request: Request):
    try:
        return templates.TemplateResponse("recovey_password.html",{"request": request})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"auth_form"},"error":error}})
    
    
    
@frontend.post("/auth", response_model=dict, tags=["AUTH"])
async def login_for_access_token(requests: Request,username: str = Form(...),password:str = Form(...) ):
    token = api_backend.authf(username, password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_decode =api_backend.token_access_decode(token[7:])

    service_response = await home(requests)
    
    service_response.set_cookie("token",token)
    service_response.set_cookie(key='username', value=token_decode["username"], httponly=True)
    service_response.set_cookie(key='empresa', value=token_decode["empresa"]["name_fantasy"], httponly=True)
    return service_response

