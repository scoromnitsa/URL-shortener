# URL Shortener Service
Сервис для сокращения ссылок с REST API и статистикой переходов

## Возможности
- Создание коротких ссылок с автоматическим сроком действия (1 день)
- Просмотр статистики переходов (за последний час/день)
- Деактивация ссылок
- Swagger документация API
- JWT аутентификация 

### Требования
- Python 3.10+
- PostgreSQL (опционально, по умолчанию SQLite)

### Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/scoromnitsa/URL-shortener.git
   cd URL-shortener
2. Настройте окружение:
    make setup-env
3. Установите зависимости:
    make init
4. Запустите сервер:
    make run

Сервер будет доступен по адресу: http://localhost:8000

### Настройка
Основные настройки в файле .env (ОБЯЗАТЕЛЬНО использовать кодирование файла UTF-8):         
    DEBUG=True      
    SECRET_KEY=ваш_секретный_ключ            
    DATABASE_URL=sqlite:///db.sqlite3             # Для PostgreSQL: postgres://user:password@localhost/dbname          
    ALLOWED_HOSTS=localhost,127.0.0.1

### API Endpoints
    Метод	- Эндпоинт - Описание
    POST - /api/urls/ - Создать короткую ссылку
    GET - /api/urls/ - Список всех ссылок
    POST - /api/urls/{id}/deactivate/ - Деактивировать ссылку
    GET - /api/stats/ - Статистика переходов
    GET - /r/{short_code}/ - Переход по короткой ссылке
Документация API: http://localhost:8000/docs/

### Команды Makefile
bash
make init          # Установка зависимостей и миграции
make run           # Запуск сервера
make generate-secret  # Сгенерировать новый SECRET_KEY
make reset-migrations # Сбросить миграции (осторожно!)
