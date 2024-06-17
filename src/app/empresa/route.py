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
templates = Jinja2Templates(directory=["src/app/empresa/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/empresa",)
async def empresa_list(request: Request):
    try:
        data = api_backend.get_empresa(filters={})
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"empresa_list"},"error":error}})

@frontend.get("/empresa/form",)
async def empresa_form(request: Request):
    try:
        empresa_data={"items":[{}]}
        status_data=api_backend.get_status(filters={})
        if(len(request.query_params) !=0 ):
            empresa_data = api_backend.get_empresa(filters=request.query_params)
         
        return templates.TemplateResponse("form.html",{"request": request,"status_data":status_data["items"],"empresa_data":empresa_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"empresa_form"},"error":error}})
    
@frontend.post("/empresa/insert")
async def empresa_insert(request: Request):
    try:
        data = dict(await request.form())
        empresa_data = api_backend.post_empresa(data=data)
        flash(request, "EMPRESA INSERIDA COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/empresa', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"empresa_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"empresa_insert"},"error":error}})
    

@frontend.post("/empresa/update/{id}")
async def empresa_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        api_backend.patch_empresa(id=id,data=data)
        flash(request, "EMPRESA ALTERADA COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/empresa', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"empresa_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"empresa_update"},"error":error}})