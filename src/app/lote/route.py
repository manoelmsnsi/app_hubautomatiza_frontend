import csv
from io import StringIO
import logging
import os
from pathlib import Path
import shutil
from typing import List, Optional
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, RedirectResponse
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
        token_decode  = await api_backend.token_access_decode(token=token[7:])

        data = await api_backend.get_lote(filters=request.query_params._dict,token = token)
            
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

@frontend.get("/lote/download",)
async def lote_form(request: Request):
    try:
        save_folder = Path(f"{os.environ.get('PATH_FILE')}/lote/output")
        lote_id=request.query_params.get("lote_id",0)
        tarefa_data = await api_backend.get_tarefa(filters=request.query_params._dict,token = request.state.token)
        csv_data = json_to_csv(tarefa_data["items"])
        save_csv_to_file(csv_content= csv_data, filename=f"lote_{lote_id}.csv", directory=f"{save_folder}/")        
        return FileResponse(f"{save_folder}/lote_{lote_id}.csv", filename=f"lote_{lote_id}.csv", headers={"Content-Disposition":f"attachment; filename=lote_{lote_id}.csv"})

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
    
def save_csv_to_file(csv_content: str, filename: str, directory: str) -> str:
        """
        Salva o conteúdo CSV em um arquivo.

        :param csv_content: O conteúdo CSV como uma string.
        :param filename: O nome do arquivo a ser salvo (com extensão .csv).
        :param directory: O diretório onde o arquivo será salvo.
        :return: O caminho completo do arquivo salvo.
        """
        # Cria o diretório se não existir
        os.makedirs(directory, exist_ok=True)

        # Caminho completo do arquivo
        file_path = os.path.join(directory, filename)

        # Salva o conteúdo CSV no arquivo
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(csv_content)

        return file_path
def flatten_json(nested_json, parent_key='', sep='_'):
        """
        Função recursiva para achatar um JSON aninhado.
        """
        items = []
        for k, v in nested_json.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

def json_to_csv(tarefas):
        # StringIO para escrever o CSV na memória
        csv_output = StringIO()
        
        # Lista de todas as chaves únicas dentro de 'response_'
        all_keys = set()

        # Função para extrair as chaves do 'response_' de cada tarefa e achatar o JSON
        def extract_keys(response_json):
            if isinstance(response_json, dict):
                flat_json = flatten_json(response_json)
                for key in flat_json.keys():
                    all_keys.add(key)

        # Primeira passagem para coletar todas as chaves dentro de 'response_' de cada tarefa
        for tarefa in tarefas:
            response_json = tarefa["response_"]
            if response_json:
                extract_keys(response_json)

        # Ordenar as chaves (opcional, para garantir ordem consistente)
        fieldnames = sorted(all_keys)
        
        # Criar o writer CSV
        writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
        
        # Escrever o cabeçalho
        writer.writeheader()

        # Função para extrair valores do 'response_' de cada tarefa e achatar o JSON
        def extract_values(response_json):
            row = {}
            if isinstance(response_json, dict):
                flat_json = flatten_json(response_json)
                for key in fieldnames:
                    row[key] = flat_json.get(key, "")
            return row

        # Segunda passagem para escrever os dados no CSV
        for tarefa in tarefas:
            response_json = tarefa["response_"]
            if response_json:
                row = extract_values(response_json)
                writer.writerow(row)
        
        # Retorna o CSV como string
        csv_content = csv_output.getvalue()

        # Debug: imprime o CSV gerado
        print("CSV gerado:\n", csv_content)

        return csv_content

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