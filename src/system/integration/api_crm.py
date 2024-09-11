import os
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
            self.auth()
            url = f"{self.BASE_URL}/pessoa/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> get_pessoa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_pessoa','error':error})   
    def post_pessoa(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/pessoa/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_pessoa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_pessoa','error':error})   
        
    def patch_pessoa(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/pessoa?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_pessoa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_pessoa','error':error})   
   
    def get_pessoa_tipo(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/pessoa_tipo/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> get_pessoa_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_pessoa_tipo','error':error})   
        
    def post_pessoa_tipo(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/pessoa_tipo/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_pessoa_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_pessoa_tipo','error':error})   
        
    def patch_pessoa_tipo(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/pessoa_tipo?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_pessoa_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_pessoa_tipo','error':error})   
   
            
    def get_endereco(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/endereco/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_endereco -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_endereco','error':error})   
    def post_endereco(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/endereco/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_endereco -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_endereco','error':error})   
        
    def patch_endereco(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/endereco?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_endereco -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_endereco','error':error})   

    def get_contato(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/contato/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_contato -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_contato','error':error}) 
    def post_contato(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/contato/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_contato -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_contato','error':error})   
        
    def patch_contato(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/contato?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_contato -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_contato','error':error})     
    
    def get_contato_tipo(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/contato_tipo/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_contato -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_contato_tipo','error':error})   
    def post_contato_tipo(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/contato_tipo/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_contato_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_contato_tipo','error':error})   
        
    def patch_contato_tipo(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/contato_tipo?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_contato_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_contato_tipo','error':error})   
       
    def get_caixa(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/caixa/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_caixa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_caixa','error':error})   
    
    def post_caixa(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/caixa/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_caixa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_caixa','error':error})   
        
    def patch_caixa(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/caixa?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_caixa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_caixa','error':error})   
    def post_processar_conta(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/conta_processar_pagamento"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_processar_conta -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_processar_conta','error':error})   
       
    def get_caixa_historico(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/caixa_historico/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_caixa_historico -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_caixa_historico','error':error})   

    def get_conta(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/conta/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_conta -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_conta','error':error})   
    def post_conta(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/conta/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_conta -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_conta','error':error})   
        
    def patch_conta(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/conta?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_conta -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_conta','error':error})   
        
    def get_conta_tipo(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/conta_tipo/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_conta_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_conta_tipo','error':error})   
    
    def post_conta_tipo(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/conta_tipo/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_conta_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_conta_tipo','error':error})   
        
    def patch_conta_tipo(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/conta_tipo?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_conta_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_conta_tipo','error':error})   
    
    def get_documento_tipo(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/documento_tipo/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_documento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_documento_tipo','error':error})   
        
    def post_documento_tipo(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/documento_tipo/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_documento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_documento_tipo','error':error})   
        
    def patch_documento_tipo(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/documento_tipo?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_documento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_documento_tipo','error':error})   

    def get_pagamento_tipo(self,filters:dict):
        try:
            self.auth()
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

    def post_pagamento_tipo(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/pagamento_tipo/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_pagamento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_pagamento_tipo','error':error})   
        
    def patch_pagamento_tipo(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/pagamento_tipo?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_pagamento_tipo -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_pagamento_tipo','error':error})    

       
    def get_categoria(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/categoria/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_categoria -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_categoria','error':error})
        
    def post_categoria(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/categoria/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_categoria -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_categoria','error':error})   
        
    def patch_categoria(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/categoria?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_categoria -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_categoria','error':error})   
       
    def get_status(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/status/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_status -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_status','error':error})
    
    def post_status(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/status/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_status -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_status','error':error})   
        
    def patch_status(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/status?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_status -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_status','error':error})   

       
    def get_empresa(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/empresa/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_empresa','error':error})
    
    def post_empresa(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/empresa/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_empresa','error':error})   
        
    def patch_empresa(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/empresa?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_empresa -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_empresa','error':error})   
        
    def get_usuario(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/usuario/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_usuario','error':error})
    
    def post_usuario(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/usuario/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_usuario','error':error})   
        
    def patch_usuario(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/usuario?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_usuario','error':error})   
        
    def get_rota(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/rota/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_rota','error':error})
    
    def post_rota(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/rota/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_rota','error':error})   
        
    def patch_rota(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/rota?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_rota','error':error})   
        
    def get_grupo_acesso(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/grupo_acesso/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_grupo_acesso -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_grupo_acesso','error':error})
    
    def post_grupo_acesso(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/grupo_acesso/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_grupo_acesso -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_grupo_acesso','error':error})   
        
    def patch_grupo_acesso(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/grupo_acesso?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_grupo_acesso -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_grupo_acesso','error':error})   
        
    def get_grupo_acesso_rota(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_rota/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_grupo_acesso_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_grupo_acesso_rota','error':error})
    
    def post_grupo_acesso_rota(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_rota/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_grupo_acesso_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_grupo_acesso_rota','error':error})   
        
    def patch_grupo_acesso_rota(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_rota?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_grupo_acesso_rota -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_grupo_acesso_rota','error':error})   
        
    def get_grupo_acesso_usuario(self,filters:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_usuario/"
            headers={"Authorization":self.TOKEN}
            payload=filters
            
            response = request(method="GET",headers=headers,url=url,params=payload)
            response.raise_for_status()    
            return response.json()
        except Exception as error:
            print(f"backend -> get_grupo_acesso_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'get_grupo_acesso_usuario','error':error})
    
    def post_grupo_acesso_usuario(self,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_usuario/"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="POST",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> post_grupo_acesso_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'post_grupo_acesso_usuario','error':error})   
        
    def patch_grupo_acesso_usuario(self,id:int,data:dict):
        try:
            self.auth()
            url = f"{self.BASE_URL}/grupo_acesso_usuario?id={id}"
            headers={
                        "Content-Type": "application/json",
                        "Authorization":self.TOKEN
                    }
            payload=data
            
            response = request(method="PATCH",headers=headers,url=url,json=payload)
            response.raise_for_status()    
            return response.json()
        
        except Exception as error:
            print(f"backend -> patch_grupo_acesso_usuario -> [ {error} ]")
            raise Exception({'integration':'backend','function':'patch_grupo_acesso_usuario','error':error})   

    
    def get_google_calendar(self,filters:dict):
        """
            filter:{
                    calendar_id:str,
                    size:int
                }
        """
        try:
            self.auth()
            url = f"{self.BASE_URL}/google_calendar/"
            headers={"Authorization":self.TOKEN}
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