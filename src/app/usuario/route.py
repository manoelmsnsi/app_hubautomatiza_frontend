from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Request, status

from src.system.core.flash import flash, get_flashed_messages
from src.system.integration.api_crm import ApiBackend





#CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG#
frontend = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
frontend.mount("/static", StaticFiles(directory="src/system/static", html=True), name="static")
templates = Jinja2Templates(directory=["src/app/usuario/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/usuario",)
async def usuario_list(request: Request):
    try:
        data = api_backend.get_usuario(filters={},token = request.state.token)
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"usuario_list"},"error":error}})

@frontend.get("/usuario/form",)
async def usuario_form(request: Request):
    try:
        usuario_data={"items":[{}]}
        empresa_data = api_backend.get_empresa(filters={},token = request.state.token)
        pessoa_data = api_backend.get_pessoa(filters={},token = request.state.token)
        status_data = api_backend.get_status(filters={},token = request.state.token)
        if(len(request.query_params) !=0 ):
            usuario_data = api_backend.get_usuario(filters=request.query_params,token = request.state.token)         
        return templates.TemplateResponse("form.html",{"request": request,"usuario_data":usuario_data["items"],"empresa_data":empresa_data["items"],"pessoa_data":pessoa_data["items"],"status_data":status_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"usuario_form"},"error":error}})
    
    
@frontend.post("/usuario/insert")
async def usuario_insert(request: Request):
    try:
        data = dict(await request.form())
        usuario_data = api_backend.post_usuario(data=data,token = request.state.token)
        flash(request, "USUARIO INSERIDO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/usuario', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"usuario_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"usuario_insert"},"error":error}})
    

@frontend.post("/usuario/update/{id}")
async def usuario_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        api_backend.patch_usuario(id=id,data=data,token = request.state.token)
        flash(request, "USUARIO ALTERADO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/usuario', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"usuario_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"usuario_update"},"error":error}})
    