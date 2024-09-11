import json
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
templates = Jinja2Templates(directory=["src/app/pessoa/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/pessoa",)
async def pessoa_list(request: Request):
    try:
        filters = {request.query_params.get("filter"):request.query_params.get("value")}
        data = api_backend.get_pessoa(filters=filters)
        return templates.TemplateResponse("list.html",{"request": request,"data":data,"filters":filters})
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
     
@frontend.post("/pessoa/insert")
async def pessoa_insert(request: Request):
    try:
        data = dict(await request.form())
        pessoa_data = api_backend.post_pessoa(data=data)
        flash(request, "PESSOA INSERIDA COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/pessoa/visualizar?id={pessoa_data["id"]}', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"pessoa_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pessoa_insert"},"error":error}})
    

@frontend.post("/pessoa/update/{id}")
async def pessoa_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        api_backend.patch_pessoa(id=id,data=data)
        flash(request, "PESSOA ALTERADA COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/pessoa/visualizar?id={id}', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"pessoa_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"pessoa_update"},"error":error}})
    

# @frontend.post("/pessoa/delete")
# async def status_insert(request: Request):
#     data = request
#     api_backend.delete_pessoa(id=id,data=request)
#     return RedirectResponse('/pessoa', status_code=status.HTTP_303_SEE_OTHER)
