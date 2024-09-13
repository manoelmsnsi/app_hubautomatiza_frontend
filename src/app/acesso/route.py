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
templates = Jinja2Templates(directory=["src/app/acesso/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/acesso",)
async def acesso_list(request: Request):
    try:
        # data = api_backend.get_acesso(filters={},token = request.state.token)
        acesso_data=api_backend.get_status(filters={},token = request.state.token)
        return templates.TemplateResponse("list.html",{"request": request,"data":acesso_data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"acesso_list"},"error":error}})

# @frontend.get("/acesso/form",)
# async def acesso_form(request: Request):
#     try:
#         acesso_data={"items":[{}]}
#         status_data=api_backend.get_status(filters={},token = request.state.token)
#         empresa_data=api_backend.get_empresa(filters={},token = request.state.token)
#         acesso_data=["LISTAR","VISUALIZAR","PROCESSAR","INSERIR","EDITAR","EXCLUIR"]
#         grupo_acesso_data=["ATENDENTE","FINANCEIRO","CAIXA","ADMIN"]
#         # if(len(request.query_params) !=0 ):
#             # acesso_data = api_backend.get_acesso(filters=request.query_params)
         
#         return templates.TemplateResponse("form.html",{"request": request,"status_data":status_data["items"],"empresa_data":empresa_data["items"],"acesso_data":acesso_data,"grupo_acesso_data":grupo_acesso_data})
#     except Exception as error:
#         return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"acesso_form"},"error":error}})
    
# @frontend.post("/status/insert")
# async def status_insert(request: Request, data_form:StatusForm = Depends(StatusForm.as_form)):
#     await status_controller.insert(data=data_form,token = request.cookies.get("token"))
#     return RedirectResponse('/status', status_code=status.HTTP_303_SEE_OTHER)

# @frontend.post("/status/update/{id}")
# async def status_update(id:int,request: Request, data_form:StatusForm = Depends(StatusForm.as_form)):
#     await status_controller.update(id=id,data=data_form,token = request.cookies.get("token"))
#     return RedirectResponse('/status', status_code=status.HTTP_303_SEE_OTHER)

# @frontend.get("/status/delete/")
# async def status_delete(id:int,request: Request)):
#     await status_controller.delete(id=id,token = request.cookies.get("token"))
#     return RedirectResponse('/status', status_code=status.HTTP_303_SEE_OTHER)
    