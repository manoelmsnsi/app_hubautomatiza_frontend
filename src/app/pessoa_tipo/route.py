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
templates = Jinja2Templates(directory=["src/app/pessoa_tipo/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/pessoa_tipo",)
async def pessoa_tipo_list(request: Request):
    try:
        data = api_backend.get_pessoa_tipo(filters={})
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pessoa_tipo_list"},"error":error}})

@frontend.get("/pessoa_tipo/form",)
async def pessoa_tipo_form(request: Request):
    try:
        pessoa_tipo_data={"items":[{}]}
        status_data=api_backend.get_status(filters={})
        if(len(request.query_params) !=0 ):
            pessoa_tipo_data = api_backend.get_pessoa_tipo(filters=request.query_params)
         
        return templates.TemplateResponse("form.html",{"request": request,"status_data":status_data["items"],"pessoa_tipo_data":pessoa_tipo_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pessoa_tipo_form"},"error":error}})
    
@frontend.post("/pessoa_tipo/insert")
async def pessoa_tipo_insert(request: Request):
    try:
        data = dict(await request.form())
        pessoa_tipo_data = api_backend.post_pessoa_tipo(data=data)
        return RedirectResponse(f'/pessoa_tipo', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"pessoa_tipo_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pessoa_tipo_insert"},"error":error}})
    

@frontend.post("/pessoa_tipo/update/{id}")
async def pessoa_tipo_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        api_backend.patch_pessoa_tipo(id=id,data=data)
        return RedirectResponse(f'/pessoa_tipo', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"pessoa_tipo_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pessoa_tipo_update"},"error":error}})