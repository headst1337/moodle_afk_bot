"""Модуль c ботом."""

import time
import random
from logging import Logger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import write_success
from config import (
    url,
    auth_url,
    username_xpath,
    password_xpath,
    login_button_xpath,
    start_test_button_xpath,
    alternative_start_test_button_xpath,
    second_alternative_start_test_button_xpath,
    navigation_button_id,
)


class Eios:
    """Класс бота для прохождения теста на платформе Eios."""
    def __init__(self, username: str, password: str, logger: Logger) -> None:
        self.username = username
        self.password = password
        self.options = webdriver.ChromeOptions()
        self.options.headless = False
        self.options.add_argument("--disable-popup-blocking")
        self.driver = webdriver.Chrome(options=self.options)
        self.log = logger
        self.__auth()

    def __auth(self) -> None:
        """Авторизация на платформе Eios."""
        self.driver.get(auth_url)
        username_element = self.driver.find_element(By.XPATH, username_xpath)
        password_element = self.driver.find_element(By.XPATH, password_xpath)
        login_button = self.driver.find_element(By.XPATH, login_button_xpath)

        username_element.send_keys(self.username)
        password_element.send_keys(self.password)

        login_button.click()

        time.sleep(random.uniform(2, 5))
        self.log.info(f"Auth as {self.username} {self.password}")
        self.__open_test()


    def __open_test(self) -> None:
        """Открытие теста."""
        self.driver.get(url)
        time.sleep(random.uniform(5, 10))

        start_test_button_xpaths = [
            start_test_button_xpath,
            alternative_start_test_button_xpath, 
            second_alternative_start_test_button_xpath
        ]

        wait = WebDriverWait(self.driver, 10)
        for xpath in start_test_button_xpaths:
            if self.__exist_element_by_xpath(xpath):
                start_test_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                start_test_button.click()
                break
        else:
            error_message = (
                f"Can not find test start button or login failed - {self.username}"
            )
            self.log.error(error_message)
            raise ValueError(error_message)

        time.sleep(random.uniform(2, 5))
        self.log.info(f"Started {self.username}")

        original_window = self.driver.current_window_handle 
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

        current_url = self.driver.current_url
        new_url = current_url.replace("page=", '')
        self.driver.get(new_url)
        self.__execution_test()


    def __execution_test(self) -> None:
        """Прохождение теста."""
        start_time = time.monotonic()
        try:
            while self.__exist_element_by_id(navigation_button_id):
                time.sleep(random.uniform(30, 270))
                self.driver.find_element(By.ID, navigation_button_id).click()
                if self.driver.current_url == auth_url:
                    error_message = f"Session timed out - {self.username}"
                    self.log.error(error_message)
                    raise ValueError(error_message)
            duration_int = time.monotonic() - start_time
            duration = self.__cacl_duration(start_time)
            self.log.info(f"Finished {self.username} in {duration}")
            if duration_int <= 1800:
                write_success(self.username, self.password)
        except:
            duration = self.__cacl_duration(start_time)
            self.log.error(f"Finished with error {self.username} in {duration}")
        finally:
            self.driver.close()
        
    def __cacl_duration(self, start_time: float) -> str:
        """Расчет времени прохождения теста."""
        duration = time.strftime(
            "%H:%M:%S",
            time.gmtime(time.monotonic() - start_time)
        )
        return duration

    def __exist_element_by_id(self, element) -> bool:
        """Проверка наличия элемента по id."""
        try:
            self.driver.find_element(By.ID, element)
            return True
        except: return False

    def __exist_element_by_xpath(self, element) -> bool:
        """Проверка наличия элемента по xpath."""
        try:
            self.driver.find_element(By.XPATH, element)
            return True
        except: return False
