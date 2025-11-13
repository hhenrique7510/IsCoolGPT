from fastapi import APIRouter, HTTPException
from app.schemas.ask import AskRequest, AskResponse
from app.controllers.ask_controller import AskController

router = APIRouter()
controller = AskController()

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Endpoint principal para fazer perguntas ao assistente
    
    - **question**: Pergunta do usuário (obrigatório)
    - **context**: Contexto adicional opcional
    - **max_tokens**: Número máximo de tokens na resposta (opcional)
    """
    try:
        response = await controller.ask(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

