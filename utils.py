"""Дополнительные функции."""

def write_success(username: str, password: str):
    """Запись успешного прохождения теста в файл."""
    success_str = f"{username} {password}"

    with open("success.txt", "a", encoding="utf-8") as f:
        f.write(f"{success_str}\n")

    with open("accounts.txt", "r+", encoding="utf-8") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if line.strip() != success_str:
                f.write(line)
        f.truncate()
