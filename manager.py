import threading
from afk_bot import Eios


username_list = []
password_list = []

def parse_accounts():
    with open("accounts.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("\n", "")
            username_list.append(line.split(" ")[0])
            password_list.append(line.split(" ")[1])
    return(username_list, password_list)        


def instantiation(i):
    instance = Eios(username=username_list[i], password=password_list[i])

if __name__ == "__main__":
    parse_accounts()
    for i in range(len(password_list)):
        thread = threading.Thread(target=instantiation, args=[i])
        thread.start()