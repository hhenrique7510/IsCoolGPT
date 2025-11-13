.PHONY: help install test run docker-build docker-run docker-stop clean

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências
	pip install -r requirements.txt

test: ## Executa testes
	pytest tests/ -v

test-cov: ## Executa testes com coverage
	pytest tests/ -v --cov=app --cov-report=html

run: ## Roda a aplicação localmente
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-build: ## Constrói imagem Docker
	docker build -t iscoolgpt:latest .

docker-run: ## Roda container Docker
	docker run -p 8000:8000 --env-file .env iscoolgpt:latest

docker-compose-up: ## Inicia com docker-compose
	docker-compose up --build

docker-compose-down: ## Para docker-compose
	docker-compose down

docker-stop: ## Para todos os containers
	docker stop $$(docker ps -q --filter ancestor=iscoolgpt:latest)

clean: ## Limpa arquivos temporários
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

lint: ## Executa linter (se configurado)
	@echo "Linting não configurado. Use flake8 ou black se necessário."

format: ## Formata código (se black estiver instalado)
	@echo "Formatting não configurado. Use black se necessário."

