from collections import defaultdict
import random
from typing import Dict, List
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, Request,status

from src.system.core.flash import get_flashed_messages
from src.system.integration.api_crm import ApiBackend





#CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG#
frontend = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
frontend.mount("/static", StaticFiles(directory="src/system/static", html=True), name="static")
templates = Jinja2Templates(directory=["src/app/auth/templates","src/app/home/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/",)
async def init(request: Request):
    # data = await api_backend.read()
    return templates.TemplateResponse("login.html",{"request": request})
    # return RedirectResponse('/auth/form', status_code=status.HTTP_303_SEE_OTHER)

@frontend.get("/home",)
async def home(request: Request):
    # data_calendar = api_backend.get_google_calendar(filters={"calendar_id":"manoelmsnsi@gmail.com","size":10})
    data = api_backend.get_hub_data(filters={"empresa_id":1,"create_at":"2024-09-09"},token = request.state.token)
    
    data_calendar = [
                        {
                            "id":"1",
                            "summary":"teste - 1",
                            "start":{"dateTime":"2024-09-11T13:00:00-03:00"},
                            "end":{"dateTime":"2024-09-11T14:00:00-03:00"},
                            "description":"Olá, isso é um teste.",
                            "hangoutLink":"http://meet.teste.com",
                            "attendees":"participante1, participante 2",
                        },
                        {
                            "id":"2",
                            "summary":"teste - 2",
                            "start":{"dateTime":"2024-09-11T15:00:00-03:00"},
                            "end":{"dateTime":"2024-09-11T16:00:00-03:00"},
                            "description":"Olá, isso é um teste.",
                            "hangoutLink":"http://meet.teste.com",
                            "attendees":"participante1, participante 2",
                        },
                    ]
    
    data_chart =  organizar_dados(dados=data)
    # {
    #     "datasets": [{
    #         "data": [80, 50, 40, 30, 20],
    #         "backgroundColor": [
    #             "#191d21",
    #             "#63ed7a",
    #             "#ffa426",
    #             "#fc544b",
    #             "#6777ef"
    #         ],
    #         "label": "Totais"
    #     }],
    #     "labels": ["Black", "Green", "Yellow", "Red", "Blue"]
    # }

    return templates.TemplateResponse("home.html",{"request": request,"data_calendar":data_calendar,"data_chart":data_chart})

@frontend.get("/em_contrucao",)
async def em_contrucao(request: Request):
    return templates.TemplateResponse("em_contrucao.html",{"request": request})

def organizar_dados(dados: List[Dict]) -> Dict:
    """
    Organiza os dados para o formato desejado para gráficos.
    
    :param dados: Lista de dicionários contendo os dados.
    :return: Dicionário com a estrutura necessária para o gráfico.
    """
    resultados = {
        "datasets": [{
            "data": [],
            "backgroundColor": [
                "#191d21", "#63ed7a", "#ffa426", "#fc544b", "#6777ef"
            ],
            "label": "Totais"
        }],
        "labels": []
    }

    # Dicionário para armazenar a contagem de linhas por empresa_id e integracao_id
    contagem_por_empresa_e_integracao = defaultdict(int)

    # Iterando sobre os dados e contando as linhas por empresa_id e integracao_id
    for dado in dados:
        chave = (dado['empresa_id'], dado['integracao_id'])
        contagem_por_empresa_e_integracao[chave] += 1

    # Dicionário para armazenar a soma das contagens por empresa_id
    contagem_por_empresa = defaultdict(int)

    for (empresa_id, integracao_id), contagem in contagem_por_empresa_e_integracao.items():
        contagem_por_empresa[empresa_id] += contagem

    # Alimentando a estrutura final
    for empresa_id, total in contagem_por_empresa.items():
        resultados['datasets'][0]['data'].append(total)
        resultados['labels'].append(f" {empresa_id}")

    return resultados