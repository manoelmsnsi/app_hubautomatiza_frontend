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
@frontend.get("/",)
async def status_list(request: Request):
    # data = await api_backend.read()
    return templates.TemplateResponse("home.html",{"request": request})

@frontend.get("/home",)
async def status_list(request: Request):
    # data_calendar = api_backend.get_google_calendar(filters={"calendar_id":"manoelmsnsi@gmail.com","size":10})
    data_calendar = [
                        {
                            "id":"1",
                            "summary":"teste - 1",
                            "start":{"dateTime":"2024-06-19T13:00:00-03:00"},
                            "end":{"dateTime":"2024-06-19T14:00:00-03:00"},
                            "description":"Olá, isso é um teste.",
                            "hangoutLink":"http://meet.teste.com",
                            "attendees":"participante1, participante 2",
                        },
                        {
                            "id":"2",
                            "summary":"teste - 2",
                            "start":{"dateTime":"2024-06-20T15:00:00-03:00"},
                            "end":{"dateTime":"2024-06-20T16:00:00-03:00"},
                            "description":"Olá, isso é um teste.",
                            "hangoutLink":"http://meet.teste.com",
                            "attendees":"participante1, participante 2",
                        },
                    ]
    return templates.TemplateResponse("home.html",{"request": request,"data_calendar":data_calendar})

@frontend.get("/em_contrucao",)
async def status_list(request: Request):
    # data = await api_backend.read()
    return templates.TemplateResponse("em_contrucao.html",{"request": request})

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
    