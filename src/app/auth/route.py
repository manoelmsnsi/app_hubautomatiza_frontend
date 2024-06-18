from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Request

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
    
# @frontend.post("/auth/insert")
# async def auth_insert(request: Request, data_form:StatusForm = Depends(StatusForm.as_form)):
#     await auth_controller.insert(data=data_form,token = request.cookies.get("token"))
#     return RedirectResponse('/auth', auth_code=auth.HTTP_303_SEE_OTHER)

# @frontend.post("/auth/update/{id}")
# async def auth_update(id:int,request: Request, data_form:StatusForm = Depends(StatusForm.as_form)):
#     await auth_controller.update(id=id,data=data_form,token = request.cookies.get("token"))
#     return RedirectResponse('/auth', auth_code=auth.HTTP_303_SEE_OTHER)

# @frontend.get("/auth/delete/")
# async def auth_delete(id:int,request: Request):
#     await auth_controller.delete(id=id,token = request.cookies.get("token"))
#     return RedirectResponse('/auth', auth_code=auth.HTTP_303_SEE_OTHER)
    