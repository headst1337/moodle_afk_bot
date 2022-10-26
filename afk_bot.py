import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import logger
from config import *


log = logger.get_logger(__name__)

class Eios:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome(options=self.options)
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
        if self._exist_element_by_xpath(start_test_button_xpath):
            self.driver.find_element(By.XPATH, start_test_button_xpath).click()
        elif self._exist_element_by_xpath(alternative_start_test_button_xpath):
             self.driver.find_element(By.XPATH, alternative_start_test_button_xpath).click()
        elif self._exist_element_by_xpath(By.XPATH, second_alternative_start_test_button_xpath):
            self.driver.find_element(By.XPATH, second_alternative_start_test_button_xpath).click()
        else: log.error(f"Can not be found test start button or login failed - {self.username}")
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
        while self._exist_element_by_id(navigation_button_id):
            time.sleep(random.randint(30, 270))
            self.driver.find_element(By.ID, navigation_button_id).click()
            if self.driver.current_url == auth_url:
                log.error(f"Session timed out - {self.username}")
        # Рассчитывание продолжительности теста
        duration = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
        log.info(f"Finished {self.username} in {duration}")
        self.driver.close()
    
    def _exist_element_by_id(self, element) -> bool:
        try:
            self.driver.find_element(By.ID, element)
            return True
        except: return False

    def _exist_element_by_xpath(self, element) -> bool:
        try:
            self.driver.find_element(By.XPATH, element)
            return True
        except: return False
