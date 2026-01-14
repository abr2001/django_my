# Django проект с PostgreSQL

Пример Django проекта с настроенной PostgreSQL базой данных.

## Требования

- Python 3.12+
- PostgreSQL
- Redis (для фоновых задач Celery)
- pip (менеджер пакетов Python)

## Установка


```bash
# Запустить PostgreSQL и Redis в Docker
docker-compose up -d

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate
```


### 1. Установите необходимые системные пакеты

```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql postgresql-contrib redis-server
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройте PostgreSQL

Отредактируйте `.env` и укажите ваши настройки базы данных:

```
DB_NAME=django_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 6. Примените миграции

```bash
python manage.py migrate
```

### 7. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

### 8. Запустите сервер разработки

```bash
python manage.py runserver
```

Проект будет доступен по адресу: http://127.0.0.1:8000/

Админ-панель: http://127.0.0.1:8000/admin/

# Запустить Celery Worker
./start_celery.sh
# или
celery -A config worker --loglevel=info

# Запустить Celery Beat (планировщик)
./start_celery_beat.sh
# или
```
celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Фоновые задачи (Celery)

Проект использует Celery для выполнения фоновых задач.

**Основная задача:** Автоматическое повышение цен на 10% каждое 1-е число месяца в 00:00.

**Подробная документация:** См. `CELERY_DOCUMENTATION.md`

**Быстрый старт:**
1. Убедитесь, что Redis запущен: `sudo systemctl start redis-server`
2. Запустите Celery Worker: `./start_celery.sh`
3. Запустите Celery Beat: `./start_celery_beat.sh`

## REST API

Проект предоставляет REST API для работы с каталогом вин.

**Endpoints:**
- `GET /api/wines/` - список вин с фильтрацией
- `GET /api/wines/{id}/` - детали вина
- `GET /api/countries/` - список стран
- `GET /api/stats/` - статистика каталога

**Подробная документация:** См. `API_DOCUMENTATION.md`

## Аналитика (ClickHouse)

Проект использует ClickHouse для высокопроизводительной аналитики продаж.

**Возможности:**
- Анализ десятков тысяч заказов в день
- Материализованные представления для быстрых отчетов
- REST API для получения аналитики
- ETL задачи для синхронизации данных

**Analytics Endpoints:**
- `GET /api/analytics/daily-sales/` - статистика по дням
- `GET /api/analytics/country-sales/` - статистика по странам
- `GET /api/analytics/top-wines/` - топ продаваемых вин
- `GET /api/analytics/metrics/` - общие метрики
- `GET /api/analytics/hourly-sales/` - статистика по часам

# Синхронизировать данные
python manage.py shell
>>> from main.tasks import sync_wines_to_clickhouse, generate_sample_sales_data
>>> sync_wines_to_clickhouse.delay()
>>> generate_sample_sales_data.delay(1000)


## Настройки

Проект использует `python-decouple` для управления переменными окружения. Все чувствительные данные должны храниться в файле `.env`, который не включен в git.

База данных PostgreSQL настроена в `config/settings.py` с использованием переменных окружения.
