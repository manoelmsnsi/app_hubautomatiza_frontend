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
templates = Jinja2Templates(directory=["src/app/conta/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/conta",)
async def conta_list(request: Request):
    try:
        data = api_backend.get_conta(filters={})
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"conta_list"},"error":error}})

@frontend.get("/conta/form",)
async def conta_form(request: Request):
    try:
        conta_data={"items":[{}]}
        status_data=api_backend.get_status(filters={})
        pessoa_data=api_backend.get_pessoa(filters={})
        empresa_data=api_backend.get_empresa(filters={})
        categoria_data=api_backend.get_categoria(filters={})
        conta_tipo_data=api_backend.get_conta_tipo(filters={})
        pagamento_tipo_data=api_backend.get_pagamento_tipo(filters={})
        documento_tipo_data=api_backend.get_documento_tipo(filters={})
        if(len(request.query_params) !=0 ):
            conta_data = api_backend.get_conta(filters=request.query_params)
         
        return templates.TemplateResponse("form.html",{
                                                        "request": request,
                                                        "conta_data": conta_data["items"],
                                                        "status_data":status_data["items"],
                                                        "pessoa_data":pessoa_data["items"],
                                                        "empresa_data":empresa_data["items"],
                                                        "categoria_data":categoria_data["items"],
                                                        "conta_tipo_data":conta_tipo_data["items"],
                                                        "pagamento_tipo_data":pagamento_tipo_data["items"],
                                                        "documento_tipo_data":documento_tipo_data["items"]
                                                        }
                                        )
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"conta_form"},"error":error}})
    
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
    