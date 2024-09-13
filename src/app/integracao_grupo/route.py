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
templates = Jinja2Templates(directory=["src/app/integracao_grupo/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/integracao_grupo",)
async def integracao_grupo_list(request: Request):
    try:
        data = api_backend.get_integracao_grupo(filters={},token = request.state.token)
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"integracao_grupo_list"},"error":error}})

@frontend.get("/integracao_grupo/form",)
async def integracao_grupo_form(request: Request):
    try:
        integracao_grupo_data={"items":[{}]}
        if(len(request.query_params) !=0 ):
            integracao_grupo_data = api_backend.get_integracao_grupo(filters=request.query_params,token = request.state.token)         
        return templates.TemplateResponse("form.html",{"request": request,"integracao_grupo_data":integracao_grupo_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"integracao_grupo_form"},"error":error}})
    
@frontend.get("/integracao_grupo/visualizar",)
async def integracao_grupo_visualizar(request: Request):
    try:
        integracao_grupo_data={"items":[{}]}
        if(len(request.query_params) !=0 ):
            integracao_grupo_data = api_backend.get_integracao_grupo(filters=request.query_params,token = request.state.token)
            integracao_data = api_backend.get_integracao(filters={"integracao_grupo_id":integracao_grupo_data["items"][0]["id"]},token = request.state.token)
         
        return templates.TemplateResponse("visualizar.html",{"request": request,"integracao_data":integracao_data,"integracao_grupo_data":integracao_grupo_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"empresa_form"},"error":error}})
    
@frontend.post("/integracao_grupo/insert")
async def integracao_grupo_insert(request: Request):
    try:
        data = dict(await request.form())
        integracao_grupo_data = api_backend.post_integracao_grupo(data=data,token = request.state.token)
        flash(request, "INTEGRAÇÃO GRUPO INSERIDO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/integracao_grupo', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"integracao_grupo_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"integracao_grupo_insert"},"error":error}})
    

@frontend.post("/integracao_grupo/update/{id}")
async def integracao_grupo_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        api_backend.patch_integracao_grupo(id=id,data=data,token = request.state.token)
        flash(request, "INTEGRAÇÃO GRUPO ALTERADO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/integracao_grupo', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"integracao_grupo_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"integracao_grupo_update"},"error":error}})
    