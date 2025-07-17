from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class ProductComponent:
    def __init__(self, driver, element: WebElement):
        self.driver = driver
        self.element = element

    @property
    def title(self):
        return self.element.find_element(By.CSS_SELECTOR, "h4.card-title").text.strip()

    @property
    def price(self):
        price_span = self.element.find_element(By.CSS_SELECTOR, "span.price--withoutTax")
        return price_span.text.strip()

    @property
    def price_float(self):
        try:
            return float(self.price.replace('$', '').replace(',', ''))
        except:
            return float('inf')

    @property
    def url(self):
        return self.element.get_attribute("href")

    def click(self):
        self.element.click()