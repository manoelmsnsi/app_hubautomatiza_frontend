

import os
from fastapi import FastAPI
from datetime import timedelta
from fastapi import FastAPI, Request,status
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
from src.system.core.flash import get_flashed_messages

from src.app.home.route import frontend as home_route
from src.app.conta.route import frontend as conta_route
from src.app.caixa.route import frontend as caixa_route
from src.app.acesso.route import frontend as acesso_route
from src.app.pessoa.route import frontend as pessoa_route
from src.app.status.route import frontend as status_route
from src.app.contato.route import frontend as contato_route
from src.app.empresa.route import frontend as empresa_route
from src.app.endereco.route import frontend as endereco_route
from src.app.categoria.route import frontend as categoria_route
from src.app.conta_tipo.route import frontend as conta_tipo_route
from src.app.pessoa_tipo.route import frontend as pessoa_tipo_route
from src.app.contato_tipo.route import frontend as contato_tipo_route
from src.app.documento_tipo.route import frontend as documento_tipo_route
from src.app.pagamento_tipo.route import frontend as pagamento_tipo_route
from src.app.caixa_historico.route import frontend as caixa_historico_route

middleware = [
    Middleware(SessionMiddleware, secret_key='super-secret')
]
app = FastAPI(docs_url=None, redoc_url=None,middleware=middleware)  


app.include_router(home_route)
app.include_router(conta_route)
app.include_router(caixa_route)
app.include_router(acesso_route)
app.include_router(pessoa_route)
app.include_router(status_route)
app.include_router(contato_route)
app.include_router(empresa_route)
app.include_router(endereco_route)
app.include_router(categoria_route)
app.include_router(conta_tipo_route)
app.include_router(pessoa_tipo_route)
app.include_router(contato_tipo_route)
app.include_router(documento_tipo_route)
app.include_router(pagamento_tipo_route)
app.include_router(caixa_historico_route)


app.mount("/static", StaticFiles(directory="src/system/static", html=True), name="static")
base_templates = Jinja2Templates(directory=["src/app/automatiza/auth/templates","src/app/home/templates"])
base_templates.env.globals['get_flashed_messages'] = get_flashed_messages


# Configurar o CORS
origins = [
    "*",  # Origem do seu aplicativo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)=
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Configure o Elastic APM
ELASTIC_APM_CONFIG = { 
    'SERVICE_NAME': os.environ.get("ELASTIC_SERVICE_NAME", "front_holly_finance"),
    'SECRET_TOKEN': os.environ.get("ELASTIC_SECRET_TOKEN", ''),  # Se necessário
    'SERVER_URL': os.environ.get("ELASTIC_SERVER_URL","http://localhost:8200"),  # URL do seu servidor APM
    'SERVER_USER': os.environ.get("ELASTIC_USER", "elastic"),
    'SERVER_PASSWORD': os.environ.get("ELASTIC_PASSWORD", "changeme")
}
ELASTIC_APM = make_apm_client(ELASTIC_APM_CONFIG)
app.add_middleware(ElasticAPM, client=ELASTIC_APM)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    token = request.cookies.get("token","TOKEN TESTE")
    url = request.url.path
    if  url=="/" or url=="/auth" or "/static/" in url:
        response = await call_next(request)
        response.timeout = 60

        return response
    elif(token is not None):
        #validar autenticidade do token
        print('TOKEN EXISTENTE')
        # token = service_security.token_access_decode(token=token)
        if token == False:
            print('TOKEN ADULTERADO')
            return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)
        else:            
            # new_token = auth_controller.create_access_token(data=token,expires_delta=timedelta(minutes=auth_controller.ACCESS_TOKEN_EXPIRE_MINUTES))[0]
            print('ENVIANDO PARA ROTA')
            response = await call_next(request)
            response.timeout = 60
            # response.set_cookie("token",new_token)
            return response
    else:
        print('TOKEN INEXISTENTE')    
        return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if request.url.path == "/auth":
        return base_templates.TemplateResponse("login.html",{"request": request,"mensagem":"Usuário ou Senha Invalido!!!"})
    elif exc.status_code==404:
        return base_templates.TemplateResponse("error/404.html",{"request": request,"data":exc.__dict__})
    elif exc.status_code==401:
        return base_templates.TemplateResponse("error/401.html",{"request": request,"data":exc.__dict__})
    else :
        return base_templates.TemplateResponse("error/500.html",{"request": request,"data":exc.__dict__})
