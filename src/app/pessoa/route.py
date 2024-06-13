from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, Request,status

from src.system.core.flash import get_flashed_messages
from src.system.integration.api_crm import ApiBackend





#CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG#
frontend = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
frontend.mount("/static", StaticFiles(directory="src/system/static", html=True), name="static")
templates = Jinja2Templates(directory=["src/app/pessoa/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/pessoa",)
async def pessoa_list(request: Request):
    try:
        data = api_backend.get_pessoa(filters={})
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pessoa_list"},"error":error}})

@frontend.get("/pessoa/form",)
async def pessoa_form(request: Request):
    try:
        pessoa_data={"items":[{}]}
        status_data=api_backend.get_status(filters={})
        empresa_data=api_backend.get_empresa(filters={})
        pessoa_tipo_data=api_backend.get_pessoa_tipo(filters={})
        if(len(request.query_params) !=0 ):
            pessoa_data = api_backend.get_pessoa(filters=request.query_params)
         
        return templates.TemplateResponse("form.html",{"request": request, "pessoa_data": pessoa_data["items"],"status_data":status_data["items"],"pessoa_tipo_data":pessoa_tipo_data["items"],"empresa_data":empresa_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pessoa_form"},"error":error}})
    
@frontend.get("/pessoa/visualizar",) 
async def pessoa_form(request: Request):
    try:
        pessoa_id=request.query_params["id"]
        pessoa_data={"items":[{}]}
        status_data=api_backend.get_status(filters={}) 
        empresa_data=api_backend.get_empresa(filters={})
        pessoa_tipo_data=api_backend.get_pessoa_tipo(filters={})
        endereco_data=api_backend.get_endereco(filters={"pessoa_id":pessoa_id})
        contato_data=api_backend.get_contato(filters={"pessoa_id":pessoa_id})        
        pessoa_data = api_backend.get_pessoa(filters=request.query_params)
         
        return templates.TemplateResponse("visualizar.html",{"request": request, "pessoa_data": pessoa_data["items"],"status_data":status_data["items"],"pessoa_tipo_data":pessoa_tipo_data["items"],"empresa_data":empresa_data["items"],"endereco_data":endereco_data["items"],"contato_data":contato_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pessoa_visualizar"},"error":error}})
    
# @frontend.post("/status/insert")
# async def status_insert(request: Request, data_form:StatusForm = Depends(StatusForm.as_form)):
#     await status_controller.insert(data=data_form,token = request.cookies.get("token"))
#     return RedirectResponse('/status', status_code=status.HTTP_303_SEE_OTHER)

# @frontend.post("/status/update/{id}")
# async def status_update(id:int,request: Request, data_form:StatusForm = Depends(StatusForm.as_form)):
#     await status_controller.update(id=id,data=data_form,token = request.cookies.get("token"))
#     return RedirectResponse('/status', status_code=status.HTTP_303_SEE_OTHER)

# @frontend.get("/status/delete/")
# async def status_delete(id:int,request: Request):
#     await status_controller.delete(id=id,token = request.cookies.get("token"))
#     return RedirectResponse('/status', status_code=status.HTTP_303_SEE_OTHER)
    