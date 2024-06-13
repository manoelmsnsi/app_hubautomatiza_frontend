import os
from fastapi import HTTPException
from requests import request
from datetime import datetime, timedelta



class ApiBackend():
    def __init__(self) -> None:
        self.BASE_URL = os.environ.get("BACNKEND_BASE_URL")
        self.USERNAME=os.environ.get("BACKEND_USUARIO")
        self.PASSWORD=os.environ.get("BACKEND_SENHA")
        self.TOKEN_VENCIMENTO=datetime.now()

    def auth(self):
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
                response = request("POST",url=url,headers=headers,data=payload)
                response.raise_for_status()
                self.TOKEN = f"Bearer {response.json()['access_token']}"
                self.TOKEN_VENCIMENTO = datetime.now() + timedelta(minutes=+55)
                return f"Bearer {response.json()['access_token']}"
            else:
                return self.TOKEN
        except Exception as error:
            print(f"BACKEND -> AUTH -> [ {error} ]")
            raise Exception({'integration':'backend','function':'auth','error':error})   
        



    def get_pessoa(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/pessoa/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> get_pessoa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_pessoa','error':error})   
   
    def get_pessoa_tipo(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/pessoa_tipo/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> get_pessoa_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_pessoa_tipo','error':error})   
   
            
    def get_endereco(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/endereco/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_endereco -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_endereco','error':error})   

    def get_contato(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/contato/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_contato -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_contato','error':error})   
    
    def get_contato_tipo(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/contato_tipo/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_contato -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_contato_tipo','error':error})   

       
    def get_caixa(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/caixa/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_caixa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_caixa','error':error})   
       
    def get_caixa_historico(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/caixa_historico/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_caixa_historico -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_caixa_historico','error':error})   

    def get_conta(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/conta/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_conta -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_conta','error':error})   
    def get_conta_tipo(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/conta_tipo/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_conta_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_conta_tipo','error':error})   
    
    def get_documento_tipo(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/documento_tipo/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_documento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_documento_tipo','error':error})   

    def get_pagamento_tipo(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/pagamento_tipo/"
            headers = {
                        "Content-Type":"application/json",
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_pagamento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_pagamento_tipo','error':error})   

       
    def get_categoria(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/categoria/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_categoria -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_categoria','error':error})   

       
    def get_status(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/status/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_status -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_status','error':error})   

       
    def get_empresa(self,filters:dict):
        try:
            url = f"{self.BASE_URL}/empresa/"
            headers={}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_empresa','error':error})   

       

# teste = ApiBackend()
# response=teste.get_pessoa(filters={})
# print(response)
# response=teste.get_endereco(filters={})
# print(response)
# response=teste.get_contato(filters={})
# print(response)
# response=teste.get_caixa(filters={})
# print(response)
# response=teste.get_conta(filters={})
# print(response)
# response=teste.get_documento_tipo(filters={})
# print(response)
# response=teste.get_pagamento_tipo(filters={})
# print(response)
# response=teste.get_categoria(filters={})
# print(response)
# response=teste.get_status(filters={})
# print(response)
# response=teste.get_empresa(filters={})
# print(response)