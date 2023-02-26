import threading
from afk_bot import Eios

MAX_THREADS = 16

def instantiate(username, password, semaphore):
    with semaphore:
        instance = Eios(username=username, password=password)
        instance.run()

def run(credentials):
    semaphore = threading.Semaphore(MAX_THREADS)
    threads = [threading.Thread(target=instantiate, args=(username, password, semaphore)) for username, password in credentials]
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
            values = line.strip().split(" ", 1)
            if len(values) == 2:
                username, password = values
                credentials.append((username, password))
    return credentials



if __name__ == "__main__":
    remove_completed_accounts()
    credentials = parse_accounts()
    run(credentials)
