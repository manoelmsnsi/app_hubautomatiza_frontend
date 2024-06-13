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
templates = Jinja2Templates(directory=["src/app/home/templates","src/app/home/templates"])
templates.env.globals['get_flashed_messages'] = get_flashed_messages


api_backend = ApiBackend()


#FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED-FRONTNED#
@frontend.get("/home",)
async def status_list(request: Request):
    # data = await api_backend.read()
    return templates.TemplateResponse("home.html",{"request": request})

# async def status_insert(request: Request, data_form:StatusForm = Depends(StatusForm.as_form)):
#     await status_controller.insert(data=data_form,token = request.cookies.get("token"))
#     return RedirectResponse('/status', status_code=status.HTTP_303_SEE_OTHER)

# @frontend.post("/status/update/{id}")
# async def status_update(id:int,request: Request, data_form:StatusForm = Depends(StatusForm.as_form)):
#     await status_controller.update(id=id,data=data_form,token = request.cookies.get("token"))
#     return RedirectResponse('/status', status_code=status.HTTP_303_SEE_OTHER)

# @frontend.get("/status/delete/")
# async def status_delete(id:int,request: Request):
#     await status_controller.delete(id=id,token = request.cookies.get("token"))
#     return RedirectResponse('/status', status_code=status.HTTP_303_SEE_OTHER)
    