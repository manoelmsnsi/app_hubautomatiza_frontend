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
templates = Jinja2Templates(directory=["src/app/grupo_acesso/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/grupo_acesso",)
async def grupo_acesso_list(request: Request):
    try:
        data = api_backend.get_grupo_acesso(filters={},token = request.state.token)
        
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_list"},"error":error}})

@frontend.get("/grupo_acesso/form",)
async def grupo_acesso_form(request: Request):
    try:
        status_data = api_backend.get_status(filters={},token = request.state.token)
        empresa_data = api_backend.get_empresa(filters={},token = request.state.token)
        grupo_acesso_data={"items":[{}]}
        if(len(request.query_params) !=0 ):
            grupo_acesso_data = api_backend.get_grupo_acesso(filters=request.query_params,token = request.state.token)         
        return templates.TemplateResponse("form.html",{"request": request,"grupo_acesso_data":grupo_acesso_data["items"],"status_data":status_data["items"],"empresa_data":empresa_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_form"},"error":error}})
    
@frontend.get("/grupo_acesso/visualizar",)
async def grupo_acesso_form(request: Request):
    try:
        grupo_acesso_id=request.query_params["id"]
        grupo_acesso_data = api_backend.get_grupo_acesso(filters={"id":grupo_acesso_id},token = request.state.token)
        grupo_acesso_rota_data = api_backend.get_grupo_acesso_rota(filters={"grupo_acesso_id":grupo_acesso_id},token = request.state.token)
        grupo_acesso_usuario_data = api_backend.get_grupo_acesso_usuario(filters={"grupo_acesso_id":grupo_acesso_id},token = request.state.token)
         
        return templates.TemplateResponse("visualizar.html",{"request": request,"grupo_acesso_data":grupo_acesso_data,"grupo_acesso_rota_data":grupo_acesso_rota_data,"grupo_acesso_usuario_data":grupo_acesso_usuario_data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_form"},"error":error}})
    
    
@frontend.post("/grupo_acesso/insert")
async def grupo_acesso_insert(request: Request):
    try:
        data = dict(await request.form())
        grupo_acesso_data = api_backend.post_grupo_acesso(data=data,token = request.state.token)
        flash(request, "VINCULO CRIADO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/grupo_acesso', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"grupo_acesso_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_insert"},"error":error}})
    

@frontend.post("/grupo_acesso/update/{id}")
async def grupo_acesso_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        api_backend.patch_grupo_acesso(id=id,data=data,token = request.state.token)
        flash(request, "VINCULO ALTERADO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/grupo_acesso', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"grupo_acesso_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"grupo_acesso_update"},"error":error}})
    