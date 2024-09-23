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
        data = await api_backend.get_realtorio_consumo_integracao(filters=request.query_params,token = request.state.token)
        return templates.TemplateResponse("relatorio_consumo_integracao.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"relatorio_consumo_integracao"},"error":error}})

