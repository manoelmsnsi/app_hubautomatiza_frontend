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
templates = Jinja2Templates(directory=["src/app/rota/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/rota",)
async def rota_list(request: Request):
    try:
        data = await api_backend.get_rota(filters={},token = request.state.token)
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"rota_list"},"error":error}})

@frontend.get("/rota/form",)
async def rota_form(request: Request):
    try:
        rota_data={"items":[{}]}
        empresa_data = await api_backend.get_empresa(filters={},token = request.state.token)
        status_data = await api_backend.get_status(filters={},token = request.state.token)
        if(len(request.query_params) !=0 ):
            rota_data = await api_backend.get_rota(filters=request.query_params,token = request.state.token)
         
        return templates.TemplateResponse("form.html",{"request": request,"rota_data":rota_data["items"],"status_data":status_data["items"],"empresa_data":empresa_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"rota_form"},"error":error}})
    
    
@frontend.post("/rota/insert")
async def rota_insert(request: Request):
    try:
        data = dict(await request.form())
        rota_data = await api_backend.post_rota(data=data,token = request.state.token)
        flash(request, "ROTA INSERIDO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/rota', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"rota_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"rota_insert"},"error":error}})
    

@frontend.post("/rota/update/{id}")
async def rota_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        await api_backend.patch_rota(id=id,data=data,token = request.state.token)
        flash(request, "ROTA ALTERADO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/rota', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"rota_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"rota_update"},"error":error}})
    