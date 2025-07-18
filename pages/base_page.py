from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_url(self, url):
        self.driver.get(url)

    def find_element(self, by_locator):
        return self.wait.until(EC.presence_of_element_located(by_locator))

    def find_elements(self, by_locator):
        return self.wait.until(EC.presence_of_all_elements_located(by_locator))

    def click_element(self, by_locator):
        self.wait.until(EC.element_to_be_clickable(by_locator)).click()

    def close_popup(self, popup_close_button_locator):
        try:
            close_button = self.wait.until(EC.element_to_be_clickable(popup_close_button_locator))
            close_button.click()
            print("Pop-up cerrado exitosamente.")
        except:
            print("No se encontró el pop-up o no se pudo cerrar.")