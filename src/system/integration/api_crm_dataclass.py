
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional

@dataclass
class CaixaHistoricoIn:
    id: Optional[int] = None
    observation: Optional[str] = None
    caixa_id: Optional[int] = None
    conta_id: Optional[int] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None

@dataclass
class CaixaHistoricoOut:
    id: Optional[int] = None
    observation: Optional[str] = None
    caixa_id: Optional[int] = None
    conta_id: Optional[int] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None
    caixa: Optional[object] = None
    conta: Optional[object] = None
    status: Optional[object] = None
    empresa: Optional[object] = None
    create_at: Optional[str] = None

@dataclass
class CaixaHistoricoProcessarPagamento:
    id: Optional[int] = None
    caixa_id: Optional[int] = None
    conta_id: Optional[int] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None
    valor_pago: Optional[float] = None
    data_pagamento: Optional[date] = None
    observation: Optional[str] = None

@dataclass
class CaixaIn:
    id: Optional[int] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None

@dataclass
class CaixaOut:
    id: Optional[int] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None
    status: Optional[object] = None
    empresa: Optional[object] = None
    create_at: Optional[str] = None

@dataclass
class CategoriaIn:
    id: Optional[int] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None

@dataclass
class CategoriaOut:
    id: Optional[int] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None
    status: Optional[object] = None
    empresa: Optional[object] = None
    create_at: Optional[str] = None

@dataclass
class ContaIn:
    id: Optional[int] = None
    descricao: Optional[str] = None
    valor_parcela: Optional[float] = None
    valor_total: Optional[float] = None
    valor_pago: Optional[float] = None
    data_pagamento: Optional[date] = None
    valor_troco: Optional[float] = None
    parcela: Optional[int] = None
    parcela_total: Optional[int] = None
    data_vencimento: Optional[date] = None
    controle: Optional[str] = None
    observation: Optional[str] = None
    documento_tipo_id: Optional[int] = None
    pagamento_tipo_id: Optional[int] = None
    categoria_id: Optional[int] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None
    pessoa_id: Optional[int] = None
    conta_tipo_id: Optional[int] = None

@dataclass
class ContaOut:
    id: Optional[int] = None
    descricao: Optional[str] = None
    valor_parcela: Optional[float] = None
    valor_total: Optional[float] = None
    valor_pago: Optional[float] = None
    data_pagamento: Optional[date] = None
    valor_troco: Optional[float] = None
    parcela: Optional[int] = None
    parcela_total: Optional[int] = None
    data_vencimento: Optional[date] = None
    controle: Optional[str] = None
    observation: Optional[str] = None
    documento_tipo_id: Optional[int] = None
    pagamento_tipo_id: Optional[int] = None
    categoria_id: Optional[int] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None
    pessoa_id: Optional[int] = None
    conta_tipo_id: Optional[int] = None
    documento_tipo: Optional[object] = None
    pagamento_tipo: Optional[object] = None
    categoria: Optional[object] = None
    status: Optional[object] = None
    pessoa: Optional[object] = None
    empresa: Optional[object] = None
    conta_tipo: Optional[object] = None
    create_at: Optional[str] = None

@dataclass
class ContaPostIn:
    descricao: Optional[str] = None
    valor_total: Optional[float] = None
    data_vencimento: Optional[date] = None
    controle: Optional[str] = None
    observation: Optional[str] = None
    documento_tipo_id: Optional[int] = None
    pagamento_tipo_id: Optional[int] = None
    categoria_id: Optional[int] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None
    pessoa_id: Optional[int] = None
    conta_tipo_id: Optional[int] = None

@dataclass
class ContaTipoIn:
    id: Optional[int] = None
    description: Optional[str] = None
    status_id: Optional[int] = None

@dataclass
class ContaTipoOut:
    id: Optional[int] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    status: Optional[object] = None
    create_at: Optional[str] = None

@dataclass
class ContatoIn:
    id: Optional[int] = None
    contato: Optional[str] = None
    contato_tipo_id: Optional[int] = None
    pessoa_id: Optional[int] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None

@dataclass
class ContatoOut:
    id: Optional[int] = None
    contato: Optional[str] = None
    contato_tipo_id: Optional[int] = None
    pessoa_id: Optional[int] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None
    pessoa: Optional[object] = None
    status: Optional[object] = None
    contato_tipo: Optional[object] = None
    empresa: Optional[object] = None
    create_at: Optional[str] = None

@dataclass
class ContatoTipoIn:
    id: Optional[int] = None
    description: Optional[str] = None
    status_id: Optional[int] = None

@dataclass
class ContatoTipoOut:
    id: Optional[int] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    status: Optional[object] = None
    create_at: Optional[str] = None

@dataclass
class DocumentoTipoIn:
    id: Optional[int] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None

@dataclass
class DocumentoTipoOut:
    id: Optional[int] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None
    status: Optional[object] = None
    empresa: Optional[object] = None
    create_at: Optional[str] = None

@dataclass
class EmpresaIn:
    id: Optional[int] = None
    name_fantasy: Optional[str] = None
    razao_social: Optional[str] = None
    cnpj: Optional[str] = None
    inscricao_estatudal: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    status_id: Optional[int] = None

@dataclass
class EmpresaOut:
    id: Optional[int] = None
    name_fantasy: Optional[str] = None
    razao_social: Optional[str] = None
    cnpj: Optional[str] = None
    inscricao_estatudal: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    status_id: Optional[int] = None
    status: Optional[object] = None
    create_at: Optional[str] = None

@dataclass
class EnderecoIn:
    id: Optional[int] = None
    pais: Optional[str] = None
    cep: Optional[str] = None
    cidade: Optional[str] = None
    bairro: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    pessoa_id: Optional[int] = None
    empresa_id: Optional[int] = None
    status_id: Optional[int] = None

@dataclass
class EnderecoOut:
    id: Optional[int] = None
    pais: Optional[str] = None
    cep: Optional[str] = None
    cidade: Optional[str] = None
    bairro: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    pessoa_id: Optional[int] = None
    empresa_id: Optional[int] = None
    status_id: Optional[int] = None
    pessoa: Optional[object] = None
    status: Optional[object] = None
    empresa: Optional[object] = None
    create_at: Optional[str] = None


@dataclass
class PagamentoTipoIn:
    id: Optional[int] = None
    description: Optional[str] = None
    entrada: Optional[bool] = None
    amout: Optional[int] = None
    fees: Optional[float] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None

@dataclass
class PagamentoTipoOut:
    id: Optional[int] = None
    description: Optional[str] = None
    entrada: Optional[bool] = None
    amout: Optional[int] = None
    fees: Optional[float] = None
    status_id: Optional[int] = None
    empresa_id: Optional[int] = None
    status: Optional[object] = None
    empresa: Optional[object] = None
    create_at: Optional[str] = None