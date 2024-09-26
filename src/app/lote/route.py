import logging
import os
from pathlib import Path
import shutil
from typing import List, Optional
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, File, Request, UploadFile, status

from src.system.core.flash import flash, get_flashed_messages
from src.system.integration.api_crm import ApiBackend



#CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG#
frontend = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
frontend.mount("/static", StaticFiles(directory="src/system/static", html=True), name="static")
templates = Jinja2Templates(directory=["src/app/lote/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()

class Estructure(BaseModel):
    cpf: Optional[int] = None
    matricula: Optional[int] = None
#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/lote",)
async def lote_list(request: Request):
    try:
        token = request.state.token
        id=None
        token_decode  = await api_backend.token_access_decode(token=token[7:])
        if token_decode.get("is_admin",False)==False:
            id = token_decode.get("lote_id",0)
            data = await api_backend.get_lote(filters={"id":id},token = token)
        else:
            data = await api_backend.get_lote(filters={},token = token)
            
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"lote_list"},"error":error}})

@frontend.get("/lote/form",)
async def lote_form(request: Request):
    try:
        lote_data={"items":[{}]}
        status_data=await api_backend.get_status(filters={},token = request.state.token)
        integracao_grupo_data=await api_backend.get_integracao_grupo(filters={},token = request.state.token)
        empresa_data=await api_backend.get_empresa(filters={},token = request.state.token)
         
        return templates.TemplateResponse("form.html",{"request": request,"status_data":status_data["items"],"lote_data":lote_data["items"],"integracao_grupo_data":integracao_grupo_data["items"],"empresa_data":empresa_data["items"]})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"lote_form"},"error":error}})
@frontend.get("/lote/baixar",)
async def lote_form(request: Request):
    try:
        return RedirectResponse(f'/em_contrucao', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"lote_form"},"error":error}})

@frontend.get("/lote/visualizar",)
async def lote_form(request: Request):
    try:
        tarefa_data={"items":[{}]}
        if(len(request.query_params) !=0 ):
            tarefa_data = await api_backend.get_tarefa(filters=request.query_params._dict,token = request.state.token)
         
        return templates.TemplateResponse("visualizar.html",{"request": request,"tarefa_data":tarefa_data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"lote _visualizar"},"error":error}})
    
@frontend.post("/lote/insert")
async def lote_insert(request: Request,file: UploadFile = File(...)):
    try:
        data = dict(await request.form())
        tarefas = process_file_to_model(file=file)
    
        # return data
        del data["file"]
        lote_data = await api_backend.post_lote(data=data,token = request.state.token)
        for tarefa in tarefas:
            tarefa_data = await api_backend.post_tarefa(data={"request_":{'cpf':tarefa.cpf,'matricula':tarefa.matricula},"lote_id":lote_data["id"],"status_id":1},token = request.state.token)
        flash(request, "lote INSERIDA COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/lote', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"lote_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"lote_insert"},"error":error}})
    
def process_file_to_model(file) -> List[Estructure]:
    data = []

    # Ler o conteúdo do arquivo
    with file.file as buffer:
        for line in buffer:
            # Decodificar a linha, remover espaços em branco extras e dividir por um delimitador
            # Supondo que o arquivo tenha CPF e matrícula separados por vírgula, ex: "12345678901,12345"
            line_data = line.decode('utf-8').strip().split(';')

            # Criar uma instância do modelo Estructure a partir dos dados da linha
            try:
                structure = Estructure(cpf=int(line_data[0]), matricula=int(line_data[1]))
                data.append(structure)
            except (IndexError, ValueError) as e:
                # Tratamento de erro caso a linha não esteja no formato esperado
                logging.error(f"Erro ao processar linha: {line}. Detalhes: {e}")
    
    return data
@frontend.post("/lote/update/{id}")
async def lote_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        await api_backend.patch_lote(id=id,data=data,token = request.state.token)
        flash(request, "lote ALTERADA COM SUCESSO!", "alert-success")
        return RedirectResponse(f'/lote', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"lote_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"lote_update"},"error":error}})