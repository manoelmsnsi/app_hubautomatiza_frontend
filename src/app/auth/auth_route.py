from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Form, HTTPException, Request,status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Page, add_pagination, paginate
import zlib

# from src.app.automatiza.services.rabbitmq.rabbitmq import Rabitmq as RabbitmqBoteria
# from src.srcc.services.rabbitmq.rabbitmq import Rabitmq as RabbitmqSrcc
import zlib

from src.app.automatiza.auth.backend.auth_model import Token, TokenData
from src.app.automatiza.auth.backend.auth_controller import AuthController
from src.app.automatiza.usuario.backend.usuario_model import Usuario, UsuarioOut


from src.system.core.utils_core import UtilsCore, get_flashed_messages
from src.system.core.security_core import SecurityCore


#CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG#

# def get_flashed_messages(request: Request):
#     print(request.session)
#     return request.session.pop("_messages") if "_messages" in request.session else []

frontend = APIRouter()

frontend.mount("/static", StaticFiles(directory="src/system/static", html=True), name="static")
auth_templates = Jinja2Templates(directory=["src/app/automatiza/auth/frontend/templates","src/app/api/templates"])
auth_templates.env.globals['get_flashed_messages'] = get_flashed_messages

# service_rabbitmq_app = RabbitmqBoteria()
# service_rabbitmq_srcc = RabbitmqSrcc()
core_utils = UtilsCore()
core_security = SecurityCore()
auth_controller = AuthController()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

#FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND-FRONTEND#

@frontend.post("/auth", response_model=TokenData, tags=["AUTH"])
async def login_for_access_token(requests: Request,username: str = Form(...),password:str = Form(...) ):
    user = await auth_controller.authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_controller.ACCESS_TOKEN_EXPIRE_MINUTES)
    # dados_comprimidos = zlib.compress(f"{user}".encode("utf-8"))
    access_token, expire = auth_controller.create_access_token(
        data=user, expires_delta=access_token_expires
    )
    # dados_descomprimidos = zlib.decompress(dados_comprimidos)

    service_response = home(requests)    
    # access_token = core_security.comprimir_string(access_token)
    
    service_response.set_cookie("token",access_token)
    service_response.set_cookie(key='username', value=user["username"], httponly=True)
    service_response.set_cookie(key='empresa', value=user["empresa"][0]["name"], httponly=True)
    return service_response




@frontend.get("/")
def login(request: Request):
    return auth_templates.TemplateResponse("login.html",{"request": request})

@frontend.get("/password/recovery")
def password_recovery(request: Request):
    return auth_templates.TemplateResponse("recovey_password.html",{"request": request})
  
@frontend.get("/home")
def home(request: Request):
    return auth_templates.TemplateResponse("home.html",{"request": request})


