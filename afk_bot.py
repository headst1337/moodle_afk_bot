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
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)
        self._auth()


    def _auth(self) -> None:
        self.driver.get(auth_url)
        username_element = self.driver.find_element(By.XPATH, username_xpath)
        password_element = self.driver.find_element(By.XPATH, password_xpath)
        login_button = self.driver.find_element(By.XPATH, login_button_xpath)

        # Ввод данных авторизации
        username_element.send_keys(self.username)
        password_element.send_keys(self.password)

        # Нажатие кнопки авторизации
        login_button.click()

        time.sleep(random.uniform(2, 5))
        log.info(f"Auth as {self.username} {self.password}")
        self._open_test()


    def _open_test(self) -> None:
        # Открытие страницы с тестом
        self.driver.get(url)
        time.sleep(random.uniform(2, 5))

        # Нажатие кнопки, которая открывает тест
        start_test_button_xpaths = [start_test_button_xpath, alternative_start_test_button_xpath, 
                                    second_alternative_start_test_button_xpath]
        for xpath in start_test_button_xpaths:
            if self._exist_element_by_xpath(xpath):
                self.driver.find_element(By.XPATH, xpath).click()
                break
        else:
            error_message = f"Can not find test start button or login failed - {self.username}"
            log.error(error_message)
            raise ValueError(error_message)
        
        time.sleep(random.uniform(2, 5))
        log.info(f"Started {self.username}")
        
        # Проверка на тест, который открывается во 2-м окне
        original_window = self.driver.current_window_handle
        self.driver.switch_to.window(next(w for w in self.driver.window_handles if w != original_window))
        
        # Переход к первому заданию в тесте
        current_url = self.driver.current_url
        new_url = current_url.replace("page=", '')
        self.driver.get(new_url)
        self._execution_test()

    
    def _execution_test(self) -> None:
        start_time = time.monotonic()
        
        # Переходит на следующее задание теста
        while self._exist_element_by_id(navigation_button_id):
            time.sleep(random.uniform(30, 270))
            self.driver.find_element(By.ID, navigation_button_id).click()
            
            if self.driver.current_url == auth_url:
                error_message = f"Session timed out - {self.username}"
                log.error(error_message)
                raise ValueError(error_message)
        
        # Рассчитывание продолжительности теста
        duration = time.strftime("%H:%M:%S", time.gmtime(time.monotonic() - start_time))
        log.info(f"Finished {self.username} in {duration}")
        
        # Закрытие окна теста
        self.driver.close()
        
        # Добавление текущего аккаунта в список успешного прохождения теста
        self._write_success()

    def _write_success(self):
        with open("success.txt", "a", encoding="utf-8") as f:
            f.write(f"{self.username} {self.password}\n")
    
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
