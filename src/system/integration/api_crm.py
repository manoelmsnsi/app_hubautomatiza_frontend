import os
import pytz
import httpx
from jose import jwt
from typing import Generic, TypeVar

from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
TC = TypeVar("TC")

class APIResponseModel(BaseModel,Generic[TC]):
    status_code:int
    message:str = None
    data:TC|dict|list = None
    detail:str = None

# Função para tratar a resposta da API
def handle_response(response: httpx.Response)->APIResponseModel:
    if 200 <= response.status_code < 300:
        # Tratamento para a casa dos 200 (Sucesso)
      return response
    #   return response.json()
    elif 300 <= response.status_code < 400:
        # Tratamento para a casa dos 300 (Redirecionamento)
        raise Exception({
            "status_code": response.status_code,
            "message": "Redirection - check the new URL",
            "data": {},
            "detail": response.text
        })
    elif 400 <= response.status_code < 500:
        # Tratamento para a casa dos 400 (Erro do Cliente)
        raise Exception({
            "status_code": response.status_code,
            "message": "Client error - Something is wrong with the request.",
            "data": {},  # ou response.json(), dependendo da API
            "detail": response.text
        })
    elif 500 <= response.status_code < 600:
        # Tratamento para a casa dos 500 (Erro do Servidor)
        raise Exception({
            "status_code": response.status_code,
            "message": "Server error - Something is wrong with the server.",
            "data": {},
            "detail": response.text
        })
    else:
        # Tratamento genérico para outros status codes
        raise Exception({
            "status_code": response.status_code,
            "message": "Unexpected status code.",
            "data": {},
            "detail": response.text
        })
class ApiBackend():
    def __init__(self) -> None:
        self.BASE_URL = os.environ.get("BACNKEND_BASE_URL")
        self.USERNAME=os.environ.get("BACKEND_USUARIO")
        self.PASSWORD=os.environ.get("BACKEND_SENHA")
        self.ALGORITHM = os.environ.get("ALGORITHM", "HS256")
        self.SECRET_KEY = os.environ.get("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
        self.TIMEZONE = pytz.timezone('America/Sao_Paulo')
        self.TOKEN_VENCIMENTO=datetime.now()

    async def authf(self,username,password):
        try:
            url=f"{self.BASE_URL}/auth/token"  
            headers = {
                                    "Content-Type":"application/json",
                                    "Content-Type": "application/x-www-form-urlencoded"
                                }
            payload =  {
                            "username": username,
                            "password": password
                        }
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",url=url,headers=headers,data=payload,timeout=50)

            response.raise_for_status()

            return f"Bearer {response.json()['access_token']}"

        except Exception as error:
            print(f"BACKEND -> AUTH -> [ {error} ]")
            raise Exception({'integration':'backend','function':'auth','error':error})   
    async def auth(self):
        try:
            url=f"{self.BASE_URL}/auth/token"  
            headers = {
                                    "Content-Type":"application/json",
                                    "Content-Type": "application/x-www-form-urlencoded"
                                }
            payload =  {
                            "username": self.USERNAME,
                            "password": self.PASSWORD
                        }
            if(self.TOKEN_VENCIMENTO <= datetime.now()):
                async with httpx.AsyncClient() as client:
                    response = await client.request("POST",url=url,headers=headers,data=payload,timeout=50)
                response.raise_for_status()
                self.TOKEN = f"Bearer {response.json()['access_token']}"
                self.TOKEN_VENCIMENTO = datetime.now() + timedelta(minutes=+55)
                return f"Bearer {response.json()['access_token']}"
            else:
                return self.TOKEN
        except Exception as error:
            print(f"BACKEND -> AUTH -> [ {error} ]")
            raise Exception({'integration':'backend','function':'auth','error':error})   

    async def get_pessoa(self,filters:dict = {},token = None):
        try:
            url = f"{self.BASE_URL}/pessoa"
            headers = {"Authorization": token}
            payload = filters
            payload["size"]= 100
            page = 1
            if "page" in payload:
                page = payload["page"]
            response_data = {
            "items": [],
            "total": 0,
            "page": 1,
            "size": 50,
            "pages": 1
        }
            
            async with httpx.AsyncClient() as client:
                while True:
                    payload["page"] = page  # Define o número da página no payload
                    resp = await client.get(url, headers=headers, params=payload,timeout=50)
                    resp.raise_for_status()
                    json_response = resp.json()

                    # Adiciona os itens da página atual
                    response_data["items"].extend(json_response.get("items", []))

                    # Preenche os demais campos de controle apenas na primeira iteração
                    
                    response_data["total"] = json_response.get("total", 0)
                    response_data["size"] = json_response.get("total", 0) #response_data["size"]+json_response.get("size", 50)
                    # response_data["pages"] = 1

                    # Verifica se já processou todas as páginas
                    if int(page) >= json_response["pages"]:
                        break

                    page += 1  # Próxima página

            return response_data  # Retorna a estrutura com
        
        except Exception as error:
            print(f"backend -> get_pessoa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_pessoa','error':error})   
    async def post_pessoa(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/pessoa"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_pessoa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_pessoa','error':error})   
        
    async def patch_pessoa(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/pessoa?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_pessoa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_pessoa','error':error})   
   
    async def get_pessoa_tipo(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/pessoa_tipo"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> get_pessoa_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_pessoa_tipo','error':error})   
        
    async def post_pessoa_tipo(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/pessoa_tipo"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_pessoa_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_pessoa_tipo','error':error})   
        
    async def patch_pessoa_tipo(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/pessoa_tipo?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_pessoa_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_pessoa_tipo','error':error})   
   
            
    async def get_endereco(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/endereco"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_endereco -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_endereco','error':error})   
    async def post_endereco(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/endereco"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_endereco -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_endereco','error':error})   
        
    async def patch_endereco(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/endereco?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_endereco -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_endereco','error':error})   

    async def get_contato(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/contato"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_contato -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_contato','error':error}) 
    async def post_contato(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/contato"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_contato -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_contato','error':error})   
        
    async def patch_contato(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/contato?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_contato -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_contato','error':error})     
    
    async def get_contato_tipo(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/contato_tipo"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_contato -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_contato_tipo','error':error})   
    async def post_contato_tipo(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/contato_tipo"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_contato_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_contato_tipo','error':error})   
        
    async def patch_contato_tipo(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/contato_tipo?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_contato_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_contato_tipo','error':error})   
       
    async def get_caixa(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/caixa"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_caixa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_caixa','error':error})   
    
    async def post_caixa(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/caixa"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_caixa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_caixa','error':error})   
        
    async def patch_caixa(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/caixa?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_caixa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_caixa','error':error})   
    async def post_processar_conta(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/conta_processar_pagamento"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_processar_conta -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_processar_conta','error':error})   
       
    async def get_caixa_historico(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/caixa_historico"
            headers = {"Authorization": token}
            payload = filters
            payload["size"]= 100
            page = 1
            if "page" in payload:
                page = payload["page"]
            response_data = {
            "items": [],
            "total": 0,
            "page": 1,
            "size": 50,
            "pages": 1
        }
            
            async with httpx.AsyncClient() as client:
                while True:
                    payload["page"] = page  # Define o número da página no payload
                    resp = await client.get(url, headers=headers, params=payload,timeout=50)
                    resp.raise_for_status()
                    json_response = resp.json()

                    # Adiciona os itens da página atual
                    response_data["items"].extend(json_response.get("items", []))

                    # Preenche os demais campos de controle apenas na primeira iteração
                    
                    response_data["total"] = json_response.get("total", 0)
                    response_data["size"] = json_response.get("total", 0) #response_data["size"]+json_response.get("size", 50)
                    # response_data["pages"] = 1

                    # Verifica se já processou todas as páginas
                    if int(page) >= json_response["pages"]:
                        break

                    page += 1  # Próxima página

            return response_data  # Retorna a estrutura com
        except Exception as error:
            print(f"backend -> get_caixa_historico -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_caixa_historico','error':error})   

    async def get_conta(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/conta"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_conta -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_conta','error':error})   
    async def post_conta(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/conta"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_conta -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_conta','error':error})   
        
    async def patch_conta(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/conta?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_conta -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_conta','error':error})   
        
    async def get_conta_tipo(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/conta_tipo"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_conta_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_conta_tipo','error':error})   
    
    async def post_conta_tipo(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/conta_tipo"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_conta_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_conta_tipo','error':error})   
        
    async def patch_conta_tipo(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/conta_tipo?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_conta_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_conta_tipo','error':error})   
    
    async def get_documento_tipo(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/documento_tipo"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_documento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_documento_tipo','error':error})   
        
    async def post_documento_tipo(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/documento_tipo"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_documento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_documento_tipo','error':error})   
        
    async def patch_documento_tipo(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/documento_tipo?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_documento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_documento_tipo','error':error})   

    async def get_pagamento_tipo(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/pagamento_tipo"
            headers = {
                        "Content-Type":"application/json",
                        "Authorization":token
                    }
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_pagamento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_pagamento_tipo','error':error})  

    async def post_pagamento_tipo(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/pagamento_tipo"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_pagamento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_pagamento_tipo','error':error})   
        
    async def patch_pagamento_tipo(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/pagamento_tipo?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_pagamento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_pagamento_tipo','error':error})    

       
    async def get_categoria(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/categoria"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_categoria -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_categoria','error':error})
        
    async def post_categoria(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/categoria"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_categoria -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_categoria','error':error})   
        
    async def patch_categoria(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/categoria?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_categoria -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_categoria','error':error})   
       
    async def get_status(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/status"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_status -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_status','error':error})
    
    async def post_status(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/status"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_status -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_status','error':error})   
        
    async def patch_status(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/status?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_status -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_status','error':error})   

       
    async def get_empresa(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/empresa"
            headers={"Authorization":token}
            payload=filters
            payload["size"]=100
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_empresa','error':error})
    
    async def post_empresa(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/empresa"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_empresa','error':error})   
        
    async def patch_empresa(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/empresa?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_empresa','error':error})   
        
    async def get_lote(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/lote"
            headers={"Authorization":token}
            payload=filters
            payload["size"]=100
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_lote -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_lote','error':error})
    
    async def post_lote(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/lote"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_lote -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_lote','error':error})   
        
    async def patch_lote(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/lote?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_lote -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_lote','error':error})   
        
    async def get_lote_download(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/lote/download"
            headers={"Authorization":token}
            payload=filters
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_lote_download -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_lote_download','error':error})
    async def get_tarefa(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/tarefa"
            headers={"Authorization":token}
            payload=filters
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_tarefa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_tarefa','error':error})
    
    async def post_tarefa(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/tarefa"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_tarefa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_tarefa','error':error})   
        
    async def patch_tarefa(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/tarefa?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_tarefa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_tarefa','error':error})   
        
    async def get_usuario(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/usuario"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_usuario','error':error})
    
    async def post_usuario(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/usuario"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_usuario','error':error})   
        
    async def patch_usuario(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/usuario?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_usuario','error':error})   
        
    async def get_rota(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/rota"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_rota','error':error})
    
    async def post_rota(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/rota"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_rota','error':error})   
        
    async def patch_rota(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/rota?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_rota','error':error})   
        
    async def get_grupo_acesso(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/grupo_acesso"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_grupo_acesso -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_grupo_acesso','error':error})
    
    async def post_grupo_acesso(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/grupo_acesso"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_grupo_acesso -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_grupo_acesso','error':error})   
        
    async def patch_grupo_acesso(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/grupo_acesso?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_grupo_acesso -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_grupo_acesso','error':error})   
        
    async def get_grupo_acesso_rota(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_rota"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_grupo_acesso_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_grupo_acesso_rota','error':error})
    
    async def post_grupo_acesso_rota(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_rota"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_grupo_acesso_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_grupo_acesso_rota','error':error})   
        
    async def patch_grupo_acesso_rota(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_rota?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_grupo_acesso_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_grupo_acesso_rota','error':error})   
        
    async def get_grupo_acesso_usuario(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_usuario"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_grupo_acesso_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_grupo_acesso_usuario','error':error})
    
    async def post_grupo_acesso_usuario(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_usuario"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_grupo_acesso_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_grupo_acesso_usuario','error':error})   
        
    async def patch_grupo_acesso_usuario(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_usuario?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_grupo_acesso_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_grupo_acesso_usuario','error':error})   
        
    async def get_integracao(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_integracao -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_integracao','error':error})
    
    async def post_integracao(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_integracao -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_integracao','error':error})   
        
    async def patch_integracao(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_integracao -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_integracao','error':error})   
        
    async def get_integracao_grupo(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao_grupo"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_integracao_grupo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_integracao_grupo','error':error})
    
    async def post_integracao_grupo(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao_grupo"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_integracao_grupo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_integracao_grupo','error':error})   
        
    async def patch_integracao_grupo(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao_grupo?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_integracao_grupo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_integracao_grupo','error':error})   
        
    async def get_integracao_saldo_empresa(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao_saldo_empresa"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_integracao_saldo_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_integracao_saldo_empresa','error':error})
    
    async def post_integracao_saldo_empresa(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao_saldo_empresa"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_integracao_saldo_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_integracao_saldo_empresa','error':error})   
        
    async def patch_integracao_saldo_empresa(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao_saldo_empresa?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_integracao_saldo_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_integracao_saldo_empresa','error':error})   
        
    async def get_integracao_historico_saldo_empresa(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao_historico_saldo_empresa"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_integracao_historico_saldo_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_integracao_historico_saldo_empresa','error':error})
    
    async def post_integracao_historico_saldo_empresa(self,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao_historico_saldo_empresa"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="POST",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_integracao_historico_saldo_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_integracao_historico_saldo_empresa','error':error})   
        
    async def patch_integracao_historico_saldo_empresa(self,id:int,data:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/integracao_historico_saldo_empresa?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":token
                    }
            payload=data
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="PATCH",headers=headers,url=url,json=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_integracao_historico_saldo_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_integracao_historico_saldo_empresa','error':error})   

    async def get_hub_data(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/hub/data"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_hub_data -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_hub_data','error':error})
    
    
    async def get_realtorio_consumo_integracao(self,filters:dict,token = None):
        try:
            # self.auth()
            url = f"{self.BASE_URL}/relatorio/consumo_integracao"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_consumo_integracao -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_consumo_integracao','error':error})
    
    
    
    async def get_google_calendar(self,filters:dict,token = None):
        """
            filter:{
                    calendar_id:str,
                    size:int
                }
        """
        try:
            # self.auth()
            url = f"{self.BASE_URL}/google_calendar"
            headers={"Authorization":token}
            payload=filters
            
            async with httpx.AsyncClient() as client:
                response = await client.request(method="GET",headers=headers,url=url,params=payload,timeout=50)
            response.raise_for_status()    
            
            return response.json()
        except Exception as error:
            print(f"backend -> get_google_calendar -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_google_calendar','error':error})
        
    async def token_access_decode(self,token: str):
        try:
            data = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])            
            return data
        except Exception as error:
            return False 
        
    async def create_access_token(self,data:dict):
        to_encode = data
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = expire.astimezone(self.TIMEZONE)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        # self.TOKEN = f"Bearer {encoded_jwt}"
        return f"Bearer {encoded_jwt}"
# teste = ApiBackend()
# response=teste.get_pessoa(filters={},token = httpx.state.token)
# print(response)
# response=teste.get_endereco(filters={},token = httpx.state.token)
# print(response)
# response=teste.get_contato(filters={},token = httpx.state.token)
# print(response)
# response=teste.get_caixa(filters={},token = httpx.state.token)
# print(response)
# response=teste.get_conta(filters={},token = httpx.state.token)
# print(response)
# response=teste.get_documento_tipo(filters={},token = httpx.state.token)
# print(response)
# response=teste.get_pagamento_tipo(filters={},token = httpx.state.token)
# print(response)
# response=teste.get_categoria(filters={},token = httpx.state.token)
# print(response)
# response=teste.get_status(filters={},token = httpx.state.token)
# print(response)
# response=teste.get_empresa(filters={},token = httpx.state.token)
# print(response)