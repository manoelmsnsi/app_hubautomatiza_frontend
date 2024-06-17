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
templates = Jinja2Templates(directory=["src/app/status/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/status",)
async def status_list(request: Request):
    try:
        data = api_backend.get_status(filters={})
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"status_list"},"error":error}})

@frontend.get("/status/form",)
async def status_form(request: Request):
    try:
        status_data={"items":[{}]}
        if(len(request.query_params) !=0 ):
            status_data = api_backend.get_status(filters=request.query_params)
         
        return templates.TemplateResponse("form.html",{"request": request,"status_data":status_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"status_form"},"error":error}})
    
    
@frontend.post("/status/insert")
async def status_insert(request: Request):
    try:
        data = dict(await request.form())
        status_data = api_backend.post_status(data=data)
        flash(request, "STATUS INSERIDO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/status', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"status_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"status_insert"},"error":error}})
    

@frontend.post("/status/update/{id}")
async def status_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        api_backend.patch_status(id=id,data=data)
        flash(request, "STATUS ALTERADO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/status', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"status_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"status_update"},"error":error}})
    