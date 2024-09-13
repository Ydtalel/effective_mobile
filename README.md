# Проект: GitHub API и E2E тесты

## Требования

- Python 3.12 или новее
- pip
- [Playwright](https://playwright.dev)

## Установка и настройка

### 1. Клонирование репозитория

Склонируйте репозиторий на ваш локальный компьютер:

```
git clone https://github.com/Ydtalel/effective_mobile.git
cd effective_mobile
```

### 2. Установка зависимостей
Создайте виртуальное окружение и активируйте его:

python -m venv .venv
source .venv/bin/activate  # Для Windows используйте:  
.venv\Scripts\activate

Установите зависимости:

`pip install -r requirements.txt`

### 3. Настройка переменных окружения

Создайте файл .env в корневой директории проекта и добавьте туда ваши  
секретные ключи для GitHub API:

```markdown
GITHUB_USERNAME=<your_github_username>
GITHUB_TOKEN=<your_github_token>
REPO_NAME=<your_repo_name>
```
**Примечание:**  
Убедитесь, что ваш токен имеет достаточные права для выполнения
операций с репозиториями.

### 4. Установка зависимостей для Playwright
`playwright install`

### Запуск скриптов
1. Запуск GitHub API скрипта

    `python tests/github_api.py`
2. Запуск E2E тестов   
    `python tests/saucedemo.py`