import logging
import requests
from decouple import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GITHUB_USERNAME = config('GITHUB_USERNAME')
GITHUB_TOKEN = config('GITHUB_TOKEN')
REPO_NAME = config('REPO_NAME')
BASE_URL = "https://api.github.com"
REPOS_URL = f"{BASE_URL}/user/repos"
REPO_URL = f"{BASE_URL}/repos/{GITHUB_USERNAME}/{REPO_NAME}"


def create_repository():
    """Создает новый репозиторий на GitHub"""
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }
    data = {
        "name": REPO_NAME,
        "description": "This is your first repo!",
        "homepage": "https://github.com",
        "private": False,
        "is_template": True
    }
    try:
        response = requests.post(REPOS_URL, json=data, headers=headers)
        response.raise_for_status()
        logger.info(f"Repository '{REPO_NAME}' created successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create repository: {e}")
        logger.debug(response.json())


def check_repository_exists():
    """Проверяет, существует ли репозиторий на GitHub"""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        response = requests.get(REPO_URL, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            logger.info(f"Repository '{REPO_NAME}' exists.")
        else:
            logger.warning(f"Repository '{REPO_NAME}' does not exist.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to check repository: {e}")
        logger.debug(response.json())


def delete_repository():
    """Удаляет репозиторий на GitHub"""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        response = requests.delete(REPO_URL, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            logger.info(f"Repository '{REPO_NAME}' deleted successfully.")
        else:
            logger.warning("Failed to delete repository. Status code:"
                           f" {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to delete repository: {e}")
        logger.debug(response.json())


def main():
    """Основная функция для управления репозиторием"""
    create_repository()
    check_repository_exists()
    delete_repository()


if __name__ == "__main__":
    main()
