
.PHONY: init run generate-secret setup-env reset-migrations check-env create-superuser install-deps test

# Проверка активации virtualenv
check-env:
	@if [ -z "$(VIRTUAL_ENV)" ]; then \
		echo "ERROR: Virtualenv не активирован. Сначала выполните:"; \
		echo "python -m venv venv && source venv/bin/activate"; \
		exit 1; \
	fi

# Генерация нового SECRET_KEY
generate-secret:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
	fi
	@if ! grep -q "SECRET_KEY=" .env; then \
		echo "SECRET_KEY=$$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")" >> .env; \
	else \
		echo "SECRET_KEY уже существует в .env"; \
	fi

# Установка зависимостей
install-deps: check-env
	pip install -r requirements.txt
	pip install psycopg2-binary  # для PostgreSQL (опционально)

# Создание .env файла
setup-env: generate-secret
	@echo "Файл .env настроен"

# Создание суперпользователя
create-superuser: check-env
	@echo "Создание суперпользователя..."
	@echo "from django.contrib.auth import get_user_model; \
	User = get_user_model(); \
	if not User.objects.filter(username='admin').exists(): \
		User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" \
	| python manage.py shell
	@echo "Суперпользователь создан: admin / admin123"

# Инициализация проекта
init: check-env setup-env install-deps
	python manage.py migrate
	@echo "Проект инициализирован. Для создания суперпользователя выполните: make create-superuser"

# Запуск сервера
run: check-env
	python manage.py runserver

# Сброс миграций
reset-migrations: check-env
	@read -p "ВНИМАНИЕ: Это удалит ВСЕ миграции. Продолжить? [y/N] " ans; \
	if [ "$$ans" = "y" ]; then \
		find . -path "*/migrations/*.py" -not -name "__init__.py" -delete; \
		find . -path "*/migrations/*.pyc" -delete; \
		python manage.py makemigrations; \
		python manage.py migrate; \
		echo "Миграции сброшены"; \
	else \
		echo "Отменено"; \
	fi