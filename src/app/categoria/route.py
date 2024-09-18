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
templates = Jinja2Templates(directory=["src/app/categoria/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/categoria",)
async def categoria_list(request: Request):
    try:
        data = await api_backend.get_categoria(filters={},token = request.state.token)
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"categoria_list"},"error":error}})

@frontend.get("/categoria/form",)
async def categoria_form(request: Request):
    try:
        categoria_data={"items":[{}]}
        status_data=await api_backend.get_status(filters={},token = request.state.token)
        empresa_data=await api_backend.get_empresa(filters={},token = request.state.token)
        if(len(request.query_params) !=0 ):
            categoria_data = await api_backend.get_categoria(filters=request.query_params,token = request.state.token)
         
        return templates.TemplateResponse("form.html",{"request": request,"status_data":status_data["items"],"empresa_data":empresa_data["items"],"categoria_data":categoria_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"categoria_form"},"error":error}})
    
@frontend.post("/categoria/insert")
async def categoria_insert(request: Request):
    try:
        data = dict(await request.form())
        categoria_data = await api_backend.post_categoria(data=data,token = request.state.token)
        flash(request, "CATEGORIA INSERIDA COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/categoria', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"categoria_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"categoria_insert"},"error":error}})
    

@frontend.post("/categoria/update/{id}")
async def categoria_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        await api_backend.patch_categoria(id=id,data=data,token = request.state.token)
        flash(request, "CATEGORIA ALTERADA COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/categoria', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"categoria_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"categoria_update"},"error":error}})