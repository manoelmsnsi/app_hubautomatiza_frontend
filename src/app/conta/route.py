from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, Request,status

from src.system.core.flash import flash, get_flashed_messages
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
        filters={}
        if len(request.query_params)!=0:
            filters = {request.query_params.get("filter"):request.query_params.get("value")}
        filters["status_id"]=1
        data = await api_backend.get_conta(filters=filters,token = request.state.token)
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"conta_list"},"error":error}})

@frontend.get("/conta/form",)
async def conta_form(request: Request):
    try:
        conta_data={"items":[{}]}
        status_data=await api_backend.get_status(filters={},token = request.state.token)
        pessoa_data=await api_backend.get_pessoa(filters={},token = request.state.token)
        empresa_data=await api_backend.get_empresa(filters={},token = request.state.token)
        categoria_data=await api_backend.get_categoria(filters={},token = request.state.token)
        conta_tipo_data=await api_backend.get_conta_tipo(filters={},token = request.state.token)
        caixa_data=await api_backend.get_caixa(filters={},token = request.state.token)
        pagamento_tipo_data=await api_backend.get_pagamento_tipo(filters={},token = request.state.token)
        documento_tipo_data=await api_backend.get_documento_tipo(filters={},token = request.state.token)
        if(len(request.query_params) !=0 ):
            conta_data = await api_backend.get_conta(filters=request.query_params,token = request.state.token)
         
        return templates.TemplateResponse("form.html",{
                                                        "request": request,
                                                        "conta_data": conta_data["items"],
                                                        "status_data":status_data["items"],
                                                        "pessoa_data":pessoa_data["items"],
                                                        "empresa_data":empresa_data["items"],
                                                        "categoria_data":categoria_data["items"],
                                                        "conta_tipo_data":conta_tipo_data["items"],
                                                        "caixa_data":caixa_data["items"],
                                                        "pagamento_tipo_data":pagamento_tipo_data["items"],
                                                        "documento_tipo_data":documento_tipo_data["items"]
                                                        }
                                        )
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"conta_form"},"error":error}})
    
@frontend.post("/conta/insert")
async def conta_insert(request: Request):
    try:
        data = dict(await request.form())
        conta_data = await api_backend.post_conta(data=data,token = request.state.token)
        flash(request, "CONTA INSERIDA COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/conta', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"conta_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"conta_insert"},"error":error}})
    
@frontend.post("/conta/update/{id}")
async def conta_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        await api_backend.patch_conta(id=id,data=data,token = request.state.token)
        flash(request, "CATEGORIA ALTERADA COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/conta', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"conta_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"conta_update"},"error":error}})
    

@frontend.post("/conta/processar")
async def conta_processar(request: Request):
    try:
        data = dict(await request.form())
        await api_backend.post_processar_conta(data=data,token = request.state.token)
        flash(request, "CONTA PROCESSADA COM SUCESSO!", "alert-sucess")
        return RedirectResponse(f'/conta', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"conta_processar"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"conta_processar"},"error":error}})