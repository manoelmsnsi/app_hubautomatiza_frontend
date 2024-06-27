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
templates = Jinja2Templates(directory=["src/app/grupo_acesso_usuario/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/grupo_acesso_usuario",)
async def grupo_acesso_usuario_list(request: Request):
    try:
        data = api_backend.get_grupo_acesso_usuario(filters={})
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_usuario_list"},"error":error}})

@frontend.get("/grupo_acesso_usuario/form",)
async def grupo_acesso_usuario_form(request: Request):
    try:
        grupo_acesso_usuario_data={"items":[{}]}
        if(len(request.query_params) !=0 ):
            grupo_acesso_usuario_data = api_backend.get_grupo_acesso_usuario(filters=request.query_params)
         
        return templates.TemplateResponse("form.html",{"request": request,"grupo_acesso_usuario_data":grupo_acesso_usuario_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_usuario_form"},"error":error}})
    
    
@frontend.post("/grupo_acesso_usuario/insert")
async def grupo_acesso_usuario_insert(request: Request):
    try:
        data = dict(await request.form())
        grupo_acesso_usuario_data = api_backend.post_grupo_acesso_usuario(data=data)
        flash(request, "grupo_acesso_usuario INSERIDO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/grupo_acesso_usuario', grupo_acesso_usuario_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"grupo_acesso_usuario_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_usuario_insert"},"error":error}})
    

@frontend.post("/grupo_acesso_usuario/update/{id}")
async def grupo_acesso_usuario_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        api_backend.patch_grupo_acesso_usuario(id=id,data=data)
        flash(request, "grupo_acesso_usuario ALTERADO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/grupo_acesso_usuario', grupo_acesso_usuario_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"grupo_acesso_usuario_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_usuario_update"},"error":error}})
    