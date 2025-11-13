from pydantic import BaseModel, Field
from typing import Optional

class AskRequest(BaseModel):
    question: str = Field(..., description="Pergunta do usuário", min_length=1, max_length=2000)
    context: Optional[str] = Field(None, description="Contexto adicional para a resposta")
    max_tokens: Optional[int] = Field(None, description="Número máximo de tokens na resposta")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "O que é Python?",
                "context": "Estou aprendendo programação",
                "max_tokens": 200
            }
        }

class AskResponse(BaseModel):
    answer: str = Field(..., description="Resposta do assistente")
    question: str = Field(..., description="Pergunta original")
    tokens_used: Optional[int] = Field(None, description="Número de tokens utilizados")
    model: Optional[str] = Field(None, description="Modelo utilizado")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Python é uma linguagem de programação de alto nível...",
                "question": "O que é Python?",
                "tokens_used": 150,
                "model": "gpt-3.5-turbo"
            }
        }

