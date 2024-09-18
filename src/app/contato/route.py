from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Request, status

from src.system.core.flash import get_flashed_messages
from src.system.integration.api_crm import ApiBackend





#CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG-CONFIG#
frontend = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
frontend.mount("/static", StaticFiles(directory="src/system/static", html=True), name="static")
templates = Jinja2Templates(directory=["src/app/contato/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/contato",)
async def contato_list(request: Request):
    try:
        data = await api_backend.get_contato(filters={},token = request.state.token)
        return templates.TemplateResponse("list.html",{"request": request,"data":data})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"contato_list"},"error":error}})

@frontend.get("/contato/form",)
async def contato_form(request: Request):
    try:
        contato_data={"items":[{}]}
        status_data=await api_backend.get_status(filters={},token = request.state.token)
        contato_tipo_data=await api_backend.get_contato_tipo(filters={},token = request.state.token)
        pessoa_id = request.query_params["pessoa_id"]
        if(len(request.query_params) >1 ):
            contato_data = await api_backend.get_contato(filters={"id":request.query_params["id"]},token = request.state.token)
         
        return templates.TemplateResponse("form.html",{"request": request,"status_data":status_data["items"],"contato_data":contato_data["items"],"contato_tipo_data":contato_tipo_data["items"],"pessoa_id":pessoa_id})
    except Exception as error:
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"contato_form"},"error":error}})
    
@frontend.post("/contato/insert")
async def contato_insert(request: Request):
    try:
        data = dict(await request.form())
        contato_data = await api_backend.post_contato(data=data,token = request.state.token)
        return RedirectResponse(f'/pessoa/visualizar?id={data["pessoa_id"]}', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"contato_insert"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"contato_insert"},"error":error}})
    

@frontend.post("/contato/update/{id}")
async def contato_update(request: Request,id:int):
    try:
        data = dict(await request.form())
        await api_backend.patch_contato(id=id,data=data,token = request.state.token)
        return RedirectResponse(f'/pessoa/visualizar?id={data["pessoa_id"]}', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as error:
        # flash(request, {"data":{"frontend":{"function":"contato_update"},"error":error}}, "alert-danger")
        return templates.TemplateResponse("error/500.html",{"request": request,"data":{"frontend":{"function":"contato_update"},"error":error}})