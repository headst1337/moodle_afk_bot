# Url теста
from tracemalloc import start


url = ""

# Url страницы авторизации
auth_url = "https://eios.sibsutis.ru/login/index.php"

# Xpath нуждне для работы бота
username_xpath = '//*[@id="username"]'
password_xpath = '//*[@id="password"]'
login_button_xpath = '//*[@id="loginbtn"]'
start_test_button_xpath = "//button[text()='Начать тестирование']"
alternative_start_test_button_xpath = "//button[text()='Продолжить последнюю попытку']"
navigation_button_id = 'mod_quiz-next-nav'
