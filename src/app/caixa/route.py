from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Request

from src.system.core.flash import get_flashed_messages
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
    
# @frontend.post("/caixa/insert")
# async def caixa_insert(request: Request, data_form:StatusForm = Depends(StatusForm.as_form)):
#     await caixa_controller.insert(data=data_form,token = request.cookies.get("token"))
#     return RedirectResponse('/caixa', caixa_code=caixa.HTTP_303_SEE_OTHER)

# @frontend.post("/caixa/update/{id}")
# async def caixa_update(id:int,request: Request, data_form:StatusForm = Depends(StatusForm.as_form)):
#     await caixa_controller.update(id=id,data=data_form,token = request.cookies.get("token"))
#     return RedirectResponse('/caixa', caixa_code=caixa.HTTP_303_SEE_OTHER)

# @frontend.get("/caixa/delete/")
# async def caixa_delete(id:int,request: Request):
#     await caixa_controller.delete(id=id,token = request.cookies.get("token"))
#     return RedirectResponse('/caixa', caixa_code=caixa.HTTP_303_SEE_OTHER)
    