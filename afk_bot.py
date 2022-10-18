import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from config import *
log = logging.getLogger("my_log")
log.setLevel(logging.INFO)
FH = logging.FileHandler('logs.log')
basic_formater = logging.Formatter('%(asctime)s : [%(levelname)s] : %(message)s')
FH.setFormatter(basic_formater)
log.addHandler(FH)

class Eios:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        # self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
        # self.driver = webdriver.Chrome(options=self.options)
        self.driver = webdriver.Chrome()
        self._auth()

    def _auth (self) -> None:
        self.driver.get(auth_url)
        # Ввод данных авторизации
        self.driver.find_element(By.XPATH, username_xpath).send_keys(self.username)
        self.driver.find_element(By.XPATH, password_xpath).send_keys(self.password)
        # Нажатие кнопки авторизации
        self.driver.find_element(By.XPATH, login_button_xpath).click()
        time.sleep((random.randrange(2, 5)))
        log.info(f"Auth as {self.username} {self.password}")
        self._open_test()

    def _open_test(self) -> None:
        # Открытие старницы с тестом
        self.driver.get(url)
        time.sleep(random.randrange(2, 5))
        # Нажатие кнопку, которая открывает тест
        try: self.driver.find_element(By.XPATH, start_test_button_xpath).click()
        except: self.driver.find_element(By.XPATH, alternative_start_test_button_xpath).click()
        time.sleep(random.randint(2, 5))
        log.info(f"Started {self.username}")
        # Проверка на тест, который открывается во 2-м окне
        original_window = self.driver.current_window_handle 
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break
        # Переход к первому заданию в тесте
        current_url = self.driver.current_url
        new_url = current_url.replace("page=", '')
        self.driver.get(new_url)
        self._execution_test()
    
    def _execution_test(self) -> None:
        start_time = time.time()
        # Переходит на следующее задание теста
        while True:
            time.sleep(random.randint(30, 270))
            try: 
                self.driver.find_element(By.ID, navigation_button_id).click()
            except: break
        # Рассчитывание продолжительности теста
        duration = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
        log.info(f"Finished {self.username} in {duration}")
        self.driver.close()
