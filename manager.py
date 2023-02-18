import threading
from afk_bot import Eios

def instantiate(username, password):
    instance = Eios(username=username, password=password)

def run(credentials):
    threads = [threading.Thread(target=instantiate, args=(username, password)) for username, password in credentials]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def remove_completed_accounts(completed_accounts):
    with open("accounts.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Отфильтровать успешные аккаунты
    remaining_accounts = [line for line in lines if line.split()[0] not in completed_accounts]

    # Перезаписать файл оставшимися учетными записями
    with open("accounts.txt", "w", encoding="utf-8") as f:
        f.writelines(remaining_accounts)

def get_completed_accounts():
    with open("completed_accounts.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        completed_accounts = [line.strip().split()[0] for line in lines]
    return completed_accounts

def parse_accounts():
    credentials = []
    with open("accounts.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            username, password = line.strip().split(" ")
            credentials.append((username, password))
    return credentials

if __name__ == "__main__":
    credentials = parse_accounts()
    run(credentials)
    remove_completed_accounts(get_completed_accounts())
