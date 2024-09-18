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
templates = Jinja2Templates(directory=["src/app/pagamento_tipo/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/pagamento_tipo",)
async def pagamento_tipo_list(request: Request):
    try:
        data = await api_backend.get_pagamento_tipo(filters={},token = request.state.token)
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pagamento_tipo_list"},"error":error}})

@frontend.get("/pagamento_tipo/form",)
async def pagamento_tipo_form(request: Request):
    try:
        pagamento_tipo_data={"items":[{}]}
        status_data=await api_backend.get_status(filters={},token = request.state.token)
        if(len(request.query_params) !=0 ):
            pagamento_tipo_data = await api_backend.get_pagamento_tipo(filters=request.query_params,token = request.state.token)         
        return templates.TemplateResponse("form.html",{"request": request,"status_data":status_data["items"],"pagamento_tipo_data":pagamento_tipo_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pagamento_tipo_form"},"error":error}})
    
@frontend.post("/pagamento_tipo/insert")
async def pagamento_tipo_insert(request: Request):
    try:
        data = dict(await request.form())
        pagamento_tipo_data = await api_backend.post_pagamento_tipo(data=data,token = request.state.token)
        flash(request, "TIPO DE PAGAMENTO INSERIDO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/pagamento_tipo', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"pagamento_tipo_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pagamento_tipo_insert"},"error":error}})
    

@frontend.post("/pagamento_tipo/update/{id}")
async def pagamento_tipo_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        await api_backend.patch_pagamento_tipo(id=id,data=data,token = request.state.token)
        flash(request, "TIPO DE PAGAMENTO ALTERADO COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/pagamento_tipo', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"pagamento_tipo_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pagamento_tipo_update"},"error":error}})