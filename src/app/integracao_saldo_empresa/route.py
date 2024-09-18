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
templates = Jinja2Templates(directory=["src/app/integracao_saldo_empresa/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/integracao_saldo_empresa",)
async def integracao_saldo_empresa_list(request: Request):
    try:
        data = await api_backend.get_integracao_saldo_empresa(filters={},token = request.state.token)
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"integracao_saldo_empresa_list"},"error":error}})

@frontend.get("/integracao_saldo_empresa/form",)
async def integracao_saldo_empresa_form(request: Request):
    try:
        integracao_saldo_empresa_data={"items":[{}]}
        empresa_data = await api_backend.get_empresa(filters={},token = request.state.token)
        integracao_grupo_data = await api_backend.get_integracao_grupo(filters={},token = request.state.token)
        if(len(request.query_params) !=0 ):
            integracao_saldo_empresa_data = await api_backend.get_integracao_saldo_empresa(filters=request.query_params,token = request.state.token)         
        return templates.TemplateResponse("form.html",{"request": request,"integracao_saldo_empresa_data":integracao_saldo_empresa_data["items"],"empresa_data":empresa_data["items"],"integracao_grupo_data":integracao_grupo_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"integracao_saldo_empresa_form"},"error":error}})
    
    
@frontend.post("/integracao_saldo_empresa/insert")
async def integracao_saldo_empresa_insert(request: Request):
    try:
        data = dict(await request.form())
        integracao_saldo_empresa_data = await api_backend.post_integracao_saldo_empresa(data=data,token = request.state.token)
        flash(request, "INTEGRAÇÃO SALDO EMPRESA INSERIDO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/integracao_saldo_empresa', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"integracao_saldo_empresa_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"integracao_saldo_empresa_insert"},"error":error}})
    

@frontend.post("/integracao_saldo_empresa/update/{id}")
async def integracao_saldo_empresa_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        await api_backend.patch_integracao_saldo_empresa(id=id,data=data,token = request.state.token)
        flash(request, "INTEGRAÇÃO SALDO EMPRESA ALTERADO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/integracao_saldo_empresa', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"integracao_saldo_empresa_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"integracao_saldo_empresa_update"},"error":error}})
    