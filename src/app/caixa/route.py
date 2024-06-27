from datetime import datetime
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Request,status

from src.system.core.flash import flash, get_flashed_messages
from src.system.integration.api_crm import ApiBackend





#CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG#
frontend = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
frontend.mount("/static", StaticFiles(directory="src/system/static", html=True), name="static")
templates = Jinja2Templates(directory=["src/app/caixa/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/caixa",)
async def caixa_list(request: Request):
    try:
        data = api_backend.get_caixa(filters={})
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"caixa_list"},"error":error}})

@frontend.get("/caixa/form",)
async def caixa_form(request: Request):
    try:
        caixa_data={"items":[{}]}
        status_data=api_backend.get_status(filters={})
        empresa_data=api_backend.get_empresa(filters={})
        if(len(request.query_params) !=0 ):
            caixa_data = api_backend.get_caixa(filters=request.query_params)
         
        return templates.TemplateResponse("form.html",{"request": request,"caixa_data":caixa_data["items"],"status_data":status_data["items"],"empresa_data":empresa_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"caixa_form"},"error":error}})
    
@frontend.post("/caixa/insert")
async def caixa_insert(request: Request):
    try:
        data = dict(await request.form())
        caixa_data = api_backend.post_caixa(data=data)
        return RedirectResponse(f'/caixa', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"caixa_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"caixa_insert"},"error":error}})
    

@frontend.post("/caixa/update/{id}")
async def caixa_update(request: Request,id: int):
    try:
        data = dict(await request.form())
        api_backend.patch_caixa(id=id,data=data)
        return RedirectResponse(f'/caixa', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"caixa_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"caixa_update"},"error":error}})
    

@frontend.get("/caixa/form_processar",)
async def caixa_form(request: Request):
    try:
        conta_id = request.query_params["conta_id"]
        caixa_data = api_backend.get_caixa(filters={})
        conta_data = api_backend.get_conta(filters={"id":conta_id})        
        status_data=api_backend.get_status(filters={})
        empresa_data=api_backend.get_empresa(filters={})
        data_current = datetime.now().strftime('%Y-%m-%d')
                 
        return templates.TemplateResponse("form_processar.html",{
                                                                    "request": request,
                                                                    "caixa_data":caixa_data["items"],
                                                                    "status_data":status_data["items"],
                                                                    "empresa_data":empresa_data["items"],
                                                                    "conta_data":conta_data["items"],
                                                                    "data_current":data_current
                                                                }
                                        )
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"caixa_form"},"error":error}})
