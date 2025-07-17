from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver: WebDriver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout

    def is_element_present(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def get_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator):
        element = self.get_element(locator)
        element.click()

    def get_element_text(self, locator):
        return self.get_element(locator).text.strip()

    def select_dropdown_option(self, dropdown_locator, option_text):
        from selenium.webdriver.support.ui import Select
        dropdown = Select(self.get_element(dropdown_locator))
        dropdown.select_by_visible_text(option_text)