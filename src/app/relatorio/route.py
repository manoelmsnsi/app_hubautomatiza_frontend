from datetime import datetime, timedelta
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
templates = Jinja2Templates(directory=["src/app/relatorio/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/relatorio_consumo_integracao",)
async def relatorio_consumo_integracao(request: Request):
    try:
        filters={}
        now = datetime.now()
        start_data = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        if now.month == 12: 
            end_data = start_data.replace(year=now.year + 1, month=1) - timedelta(seconds=1)
        else:
            end_data = start_data.replace(month=now.month + 1) - timedelta(seconds=1)
            
        filters["start_data"] = request.query_params.get("start_data",start_data.date())
        filters["end_data"] = request.query_params.get("end_data",end_data.date())
        

        if len(request.query_params)!=0:
            filters[request.query_params.get("filter")] = request.query_params.get("value",None)
            
    
        data = await api_backend.get_realtorio_consumo_integracao(filters=filters,token = request.state.token)
        return templates.TemplateResponse("relatorio_consumo_integracao.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"relatorio_consumo_integracao"},"error":error}})

