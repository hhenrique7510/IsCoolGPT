from typing import Optional
import httpx
from app.core.config import settings

class LLMService:
    """Serviço para integração com modelos de linguagem"""
    
    def __init__(self):
        self.provider = settings.llm_provider
        self.openai_api_key = settings.openai_api_key
        self.huggingface_api_key = settings.huggingface_api_key
        self.huggingface_api_url = settings.huggingface_api_url or "https://api-inference.huggingface.co/models"
    
    async def generate_response(
        self, 
        question: str, 
        context: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> dict:
        """
        Gera resposta usando o provedor de LLM configurado
        
        Returns:
            dict com 'answer', 'tokens_used' e 'model'
        """
        if self.provider == "openai":
            return await self._generate_openai(question, context, max_tokens)
        elif self.provider == "huggingface":
            return await self._generate_huggingface(question, context, max_tokens)
        elif self.provider == "mock":
            return await self._generate_mock(question, context, max_tokens)
        else:
            raise ValueError(f"Provedor de LLM não suportado: {self.provider}")
    
    async def _generate_openai(
        self, 
        question: str, 
        context: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> dict:
        """Gera resposta usando OpenAI API"""
        if not self.openai_api_key:
            raise ValueError("OpenAI API key não configurada")
        
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=self.openai_api_key)
            
            prompt = question
            if context:
                prompt = f"Contexto: {context}\n\nPergunta: {question}"
            
            response = await client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente educacional inteligente chamado IsCoolGPT. Responda de forma clara, didática e objetiva, sempre focando em ajudar o aprendizado."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens or settings.max_tokens,
                temperature=settings.temperature
            )
            
            return {
                "answer": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "model": response.model
            }
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta com OpenAI: {str(e)}")
    
    async def _generate_huggingface(
        self, 
        question: str, 
        context: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> dict:
        """Gera resposta usando Hugging Face API"""
        if not self.huggingface_api_key:
            raise ValueError("Hugging Face API key não configurada")
        
        try:
            model_url = f"{self.huggingface_api_url}/{settings.huggingface_model}"
            
            prompt = question
            if context:
                prompt = f"Contexto: {context}\n\nPergunta: {question}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    model_url,
                    headers={
                        "Authorization": f"Bearer {self.huggingface_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "max_new_tokens": max_tokens or settings.max_tokens,
                            "temperature": settings.temperature,
                            "return_full_text": False
                        }
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"Erro na API Hugging Face: {response.status_code} - {response.text}")
                
                result = response.json()
                
                # Extrair resposta do formato Hugging Face
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    generated_text = result.get("generated_text", str(result))
                else:
                    generated_text = str(result)
                
                return {
                    "answer": generated_text.strip(),
                    "tokens_used": None,  # Hugging Face não retorna sempre
                    "model": settings.huggingface_model
                }
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta com Hugging Face: {str(e)}")
    
    async def _generate_mock(
        self, 
        question: str, 
        context: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> dict:
        """Gera resposta mockada para testes (não requer API key)"""
        import asyncio
        
        # Simula delay de API
        await asyncio.sleep(0.5)
        
        # Respostas educacionais mockadas baseadas em palavras-chave
        question_lower = question.lower()
        
        if "python" in question_lower:
            answer = "Python é uma linguagem de programação de alto nível, interpretada e de propósito geral. É conhecida por sua sintaxe clara e legível, o que a torna ideal para iniciantes. Python suporta múltiplos paradigmas de programação, incluindo orientação a objetos, programação funcional e programação procedural."
        elif "docker" in question_lower:
            answer = "Docker é uma plataforma de containerização que permite empacotar aplicações e suas dependências em containers isolados. Isso garante que a aplicação funcione de forma consistente em diferentes ambientes, desde desenvolvimento até produção."
        elif "api" in question_lower or "rest" in question_lower:
            answer = "API REST (Representational State Transfer) é um estilo arquitetural para desenvolvimento de serviços web. Utiliza métodos HTTP (GET, POST, PUT, DELETE) para operações e retorna dados geralmente em formato JSON. É stateless, ou seja, cada requisição contém toda informação necessária."
        elif "fastapi" in question_lower:
            answer = "FastAPI é um framework web moderno e rápido para Python, baseado em type hints. Oferece alta performance, documentação automática (Swagger/OpenAPI), validação de dados com Pydantic e suporte nativo a async/await. É ideal para criar APIs REST modernas."
        elif "aws" in question_lower or "cloud" in question_lower:
            answer = "AWS (Amazon Web Services) é uma plataforma de computação em nuvem que oferece mais de 200 serviços, incluindo computação, armazenamento, bancos de dados, machine learning e muito mais. Permite escalabilidade, flexibilidade e redução de custos para empresas de todos os tamanhos."
        elif "programação" in question_lower or "código" in question_lower:
            answer = "Programação é o processo de escrever instruções que um computador pode executar. Envolve resolver problemas, pensar logicamente e usar linguagens de programação para criar software. É uma habilidade essencial na era digital e pode ser aprendida por qualquer pessoa com dedicação e prática."
        else:
            answer = f"Esta é uma resposta de demonstração do IsCoolGPT. Você perguntou: '{question}'. Em um ambiente de produção, esta resposta seria gerada por um modelo de linguagem avançado. Para usar respostas reais, configure uma chave da OpenAI ou Hugging Face no arquivo .env. Esta resposta mockada demonstra que a API está funcionando corretamente!"
        
        # Adiciona contexto se fornecido
        if context:
            answer = f"[Contexto: {context}]\n\n{answer}"
        
        # Limita tamanho se max_tokens especificado
        if max_tokens:
            words = answer.split()
            estimated_tokens = len(words) * 1.3  # Aproximação: 1 token ≈ 0.75 palavras
            if estimated_tokens > max_tokens:
                words = words[:int(max_tokens * 0.75)]
                answer = " ".join(words) + "..."
        
        return {
            "answer": answer,
            "tokens_used": int(len(answer.split()) * 1.3),  # Estimativa (convertido para int)
            "model": "mock-iscoolgpt-v1.0"
        }

