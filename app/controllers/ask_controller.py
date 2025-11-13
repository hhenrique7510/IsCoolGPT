from app.schemas.ask import AskRequest, AskResponse
from app.services.llm_service import LLMService

class AskController:
    """Controller para lidar com requisições de perguntas"""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    async def ask(self, request: AskRequest) -> AskResponse:
        """
        Processa uma pergunta e retorna uma resposta do assistente
        
        Args:
            request: AskRequest com a pergunta e contexto opcional
            
        Returns:
            AskResponse com a resposta do assistente
        """
        try:
            result = await self.llm_service.generate_response(
                question=request.question,
                context=request.context,
                max_tokens=request.max_tokens
            )
            
            return AskResponse(
                answer=result["answer"],
                question=request.question,
                tokens_used=result.get("tokens_used"),
                model=result.get("model")
            )
        except Exception as e:
            # Em produção, você pode querer usar um logger adequado
            raise Exception(f"Erro ao processar pergunta: {str(e)}")

