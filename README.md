# ShopUA — Онлайн-магазин на Django


> Повнофункціональний онлайн-магазин, розроблений у рамках лабораторної роботи з дисципліни «Неперервна інтеграція та розгортання ПЗ». Рівень: Складний.

---

## Команда

| Учасник | Відповідальність |
|---------|-----------------|
| **Корнієнко Світлана** (Учасник 1) | Django models, Admin panel, Docker, GitHub Actions (lint + docker jobs) |
| **Вялкова Поліна** (Учасник 2) | Django views, Templates, Tests, GitHub Actions (test + summary jobs) |

---

## Можливості проекту

- Каталог товарів з категоріями та пошуком
- Кошик покупок
- Система замовлень зі статусами
- Реєстрація та авторизація користувачів
- Django Admin Panel для управління

---

## Швидкий старт

### За допомогою Docker (рекомендовано)

```bash
git clone https://github.com/kornienkosvitlana20/shopua-django.git
cd shopua-django
docker compose up -d
```

Застосунок: http://localhost:8000  
Адмінпанель: http://localhost:8000/admin  
Логін: `admin` | Пароль: `admin123`

### Локально (без Docker)

```bash
# Створити та активувати віртуальне середовище
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Встановити залежності
pip install -r requirements.txt

# Застосувати міграції та заповнити тестовими даними
python manage.py migrate
python manage.py populate_data

# Запустити сервер
python manage.py runserver
```

---

## Тестування

```bash
# Запуск всіх тестів
python manage.py test shop --verbosity=2

# Запуск з покриттям коду
pip install coverage
coverage run manage.py test shop
coverage report
```

### Структура тестів

| Тест | Відповідальний | Що перевіряє |
|------|---------------|--------------|
| `CategoryModelTest` | Учасник 1 | Модель категорій |
| `ProductModelTest` | Учасник 1 | Модель товарів |
| `OrderModelTest` | Учасник 1 | Модель замовлень |
| `CartModelTest` | Учасник 1 | Модель кошика |
| `ProductListViewTest` | Учасник 2 | Список товарів |
| `ProductDetailViewTest` | Учасник 2 | Деталі товару |
| `CartViewTest` | Учасник 2 | Операції з кошиком |
| `AuthViewTest` | Учасник 2 | Авторизація |
| `OrderViewTest` | Учасник 2 | Замовлення |

---

## Docker

```bash
docker build -t shopua .       # Зібрати образ
docker compose up -d           # Запустити
docker compose logs -f         # Переглянути логи
docker compose down            # Зупинити
```

---

## CI/CD Pipeline (GitHub Actions)

```
push / PR  →  lint  →  test  →  docker-build  →  deploy-summary
```

| Job | Відповідальний | Дії |
|-----|---------------|-----|
| **lint** | Учасник 1 | Перевірка конфігурації Django |
| **test** | Учасник 2 | Запуск тестів + coverage |
| **docker-build** | Учасник 1 | Збірка образу + запуск тестів у контейнері |
| **deploy-summary** | Учасник 2 | Звіт про результати pipeline |

---

## Структура проекту

```
shopua-django/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD
├── config/
│   ├── settings.py             # Налаштування Django
│   ├── urls.py                 # Головні URL
│   └── wsgi.py
├── shop/
│   ├── models.py               # Моделі БД
│   ├── views.py                # View-функції
│   ├── urls.py                 # URL маршрути
│   ├── admin.py                # Admin panel
│   ├── forms.py                # Форми
│   ├── tests.py                # Тести
│   ├── context_processors.py   # Контекстні процесори
│   ├── templates/shop/         # HTML шаблони
│   └── management/commands/
│       └── populate_data.py    # Команда заповнення БД
├── templates/
│   ├── base.html               # Базовий шаблон
│   └── registration/           # Шаблони авторизації
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Технології

| Категорія | Технологія |
|-----------|-----------|
| Backend | Python 3.11, Django 4.2 |
| Frontend | Bootstrap 5, Bootstrap Icons |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Server | Gunicorn |

---

## Оцінювання

| Критерій | Бали |
|----------|------|
| Django веб-застосунок (складний) | 8 |
| Docker та docker-compose | 2 |
| GitHub Actions | 2 |
| Django Admin Panel | +1 (бонус) |
| **Всього** | **13** |

---

