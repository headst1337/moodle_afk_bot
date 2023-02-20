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

def remove_completed_accounts():
    with open("success.txt", "w", encoding="utf-8") as f:
        f.truncate(0)

def parse_accounts():
    credentials = []
    with open("accounts.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            username, password = line.strip().split(" ")
            credentials.append((username, password))
    return credentials

if __name__ == "__main__":
    remove_completed_accounts()
    credentials = parse_accounts()
    run(credentials)
    
