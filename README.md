### Hexlet tests and linter status:
[![Actions Status](https://github.com/SerovAA/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/SerovAA/python-project-83/actions)
---
# Анализатор страниц

**Анализатор страниц** – это веб-сайт, который анализирует веб-страницы на предмет пригодности для SEO.

Посмотреть работы на [render.com](https://page-analyzer-28ua.onrender.com)
---

## Установка

1. Склонировать репозиторий:
```
https://github.com/SerovAA/Page-Analyzer
```
2. Прейти в директорию проекта:
```
cd Page-Analyzer
```
3. Установить проект:
```
make install
```

4. Настройка переменных окружения:

Создайте файл .env в корневой директории проекта 
и добавьте туда следующие переменные окружения:

DATABASE_URL — URL для подключения к базе данных.
SECRET_KEY — секретный ключ для безопасности приложения.
---
## Запуск
Локально:
```
make dev
```

## Для применения миграции к БД
```
database.sql
```