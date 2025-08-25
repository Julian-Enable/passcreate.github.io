# Makefile para GenPassw Pro

.PHONY: install run dev test clean help

# Variables
PYTHON = python
PIP = pip
FLASK_APP = app.py

help: ## Mostrar ayuda
	@echo "🔐 GenPassw Pro - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias y configurar entorno
	@echo "📦 Instalando dependencias..."
	$(PYTHON) install.py

run: ## Ejecutar la aplicación
	@echo "🚀 Iniciando GenPassw Pro..."
	$(PYTHON) run.py

dev: ## Ejecutar en modo desarrollo
	@echo "🔧 Iniciando en modo desarrollo..."
	FLASK_ENV=development FLASK_DEBUG=1 $(PYTHON) run.py

test: ## Ejecutar tests
	@echo "🧪 Ejecutando tests..."
	$(PYTHON) -m pytest tests/ -v

clean: ## Limpiar archivos temporales
	@echo "🧹 Limpiando archivos temporales..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf logs/*.log

setup: ## Configurar proyecto completo
	@echo "🔧 Configurando proyecto completo..."
	$(MAKE) install
	@echo "✅ Configuración completada"

backup: ## Crear backup de la base de datos
	@echo "💾 Creando backup..."
	cp passwords.db backups/passwords_$(shell date +%Y%m%d_%H%M%S).db
	@echo "✅ Backup creado en backups/"

logs: ## Ver logs en tiempo real
	@echo "📋 Mostrando logs..."
	tail -f logs/genpassw_pro_$(shell date +%Y%m%d).log
