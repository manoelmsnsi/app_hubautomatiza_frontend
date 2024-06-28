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
templates = Jinja2Templates(directory=["src/app/grupo_acesso_rota/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/grupo_acesso_rota",)
async def grupo_acesso_rota_list(request: Request):
    try:
        data = api_backend.get_grupo_acesso_rota(filters={})
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_rota_list"},"error":error}})

@frontend.get("/grupo_acesso_rota/form",)
async def grupo_acesso_rota_form(request: Request):
    try:
        grupo_acesso_id = request.query_params["grupo_acesso_id"]
        grupo_acesso_rota_data = api_backend.get_grupo_acesso_rota(filters={"id":grupo_acesso_id})
        empresa_data = api_backend.get_empresa(filters={})
        grupo_acesso_data = api_backend.get_grupo_acesso(filters={})
        status_data = api_backend.get_status(filters={})
        rota_data = api_backend.get_rota(filters={})
         
        return templates.TemplateResponse("form.html",{"request": request,"grupo_acesso_rota_data":grupo_acesso_rota_data["items"],"rota_data":rota_data["items"],"empresa_data":empresa_data["items"],"grupo_acesso_data":grupo_acesso_data["items"],"status_data":status_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_rota_form"},"error":error}})
    
    
@frontend.post("/grupo_acesso_rota/insert")
async def grupo_acesso_rota_insert(request: Request):
    try:
        data = dict(await request.form())
        grupo_acesso_rota_data = api_backend.post_grupo_acesso_rota(data=data)
        flash(request, "grupo_acesso_rota INSERIDO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/grupo_acesso/visualizar?id={grupo_acesso_rota_data["grupo_acesso_id"]}', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        flash(request, {"data":{"frontend":{"function":"grupo_acesso_rota_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_rota_insert"},"error":error}})
    

@frontend.post("/grupo_acesso_rota/update/{id}")
async def grupo_acesso_rota_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        api_backend.patch_grupo_acesso_rota(id=id,data=data)
        flash(request, "grupo_acesso_rota ALTERADO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/grupo_acesso_rota', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"grupo_acesso_rota_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_rota_update"},"error":error}})
    