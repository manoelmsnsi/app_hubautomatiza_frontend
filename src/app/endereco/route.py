from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Request, status

from src.system.core.flash import get_flashed_messages
from src.system.integration.api_crm import ApiBackend





#CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG#
frontend = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
frontend.mount("/static", StaticFiles(directory="src/system/static", html=True), name="static")
templates = Jinja2Templates(directory=["src/app/endereco/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/endereco",)
async def endereco_list(request: Request):
    try:
        data = api_backend.get_endereco(filters={})
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"endereco_list"},"error":error}})

@frontend.get("/endereco/form",)
async def endereco_form(request: Request):
    try:
        endereco_data={"items":[{}]}
        status_data=api_backend.get_status(filters={})
        pessoa_id = request.query_params["pessoa_id"]
        if(len(request.query_params) >1 ):
            endereco_data = api_backend.get_endereco(filters={"id":request.query_params["id"]})
         
        return templates.TemplateResponse("form.html",{"request": request,"status_data":status_data["items"],"endereco_data":endereco_data["items"],"pessoa_id":pessoa_id})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"endereco_form"},"error":error}})
    
@frontend.post("/endereco/insert")
async def endereco_insert(request: Request):
    try:
        data = dict(await request.form())
        endereco_data = api_backend.post_endereco(data=data)
        return RedirectResponse(f'/pessoa/visualizar?id={data["pessoa_id"]}', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"endereco_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"endereco_insert"},"error":error}})
    

@frontend.post("/endereco/update/{id}")
async def endereco_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        api_backend.patch_endereco(id=id,data=data)
        return RedirectResponse(f'/pessoa/visualizar?id={data["pessoa_id"]}', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"endereco_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"endereco_update"},"error":error}})