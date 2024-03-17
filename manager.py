"""Точка входа и создание экземпляров бота."""

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
from logging import Logger

from afk_bot import Eios
from logger import get_logger


MAX_THREADS = 16 # Константа для ограничения количества потоков.
TRYIES = 2 # Константа для ограничения количества попыток.


def instantiate(username: str,password: str, logger: Logger) -> None:
    """Создание экземпляра бота и запуск теста."""
    Eios(username=username, password=password, logger=logger)


def run(credentials: list[tuple[str, str]], logger: Logger) -> None:
    """Создание потоков для каждого аккаунта."""
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        for username, password in credentials:
            futures.append(executor.submit(instantiate, username, password, logger))

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")


def remove_completed_accounts() -> None:
    """Очистка файла success.txt."""
    with open("success.txt", "w", encoding="utf-8") as f:
        f.truncate(0)


def parse_accounts() -> list[tuple[str, str]]:
    """Парсинг аккаунтов из файла accounts.txt."""
    credentials = []
    with open("accounts.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            values = line.strip().split(" ", maxsplit=1)
            if len(values) == 2:
                username, password = values
                credentials.append((username, password))
    return credentials


if __name__ == "__main__":
    remove_completed_accounts()
    logger = get_logger(__name__)
    for _ in range(TRYIES):
        credentials = parse_accounts()
        run(credentials, logger)
