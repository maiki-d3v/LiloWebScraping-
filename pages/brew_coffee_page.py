import time

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config.settings import settings

class BrewCoffeePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        if settings.POPUP_CLOSE_BUTTON_SELECTOR and ("/" in settings.POPUP_CLOSE_BUTTON_SELECTOR or "[" in settings.POPUP_CLOSE_BUTTON_SELECTOR):
            self.POPUP_CLOSE_BUTTON = (By.XPATH, settings.POPUP_CLOSE_BUTTON_SELECTOR)
        else:
            self.POPUP_CLOSE_BUTTON = (By.CSS_SELECTOR, settings.POPUP_CLOSE_BUTTON_SELECTOR) if settings.POPUP_CLOSE_BUTTON_SELECTOR else None

        if settings.SORT_DROPDOWN_SELECTOR and ("/" in settings.SORT_DROPDOWN_SELECTOR or "[" in settings.SORT_DROPDOWN_SELECTOR):
            self.SORT_DROPDOWN = (By.XPATH, settings.SORT_DROPDOWN_SELECTOR)
        else:
            self.SORT_DROPDOWN = (By.CSS_SELECTOR, settings.SORT_DROPDOWN_SELECTOR) if settings.SORT_DROPDOWN_SELECTOR else None

        if settings.PRODUCT_DIV_SELECTOR and ("/" in settings.PRODUCT_DIV_SELECTOR or "[" in settings.PRODUCT_DIV_SELECTOR):
            self.PRODUCT_DIV = (By.XPATH, settings.PRODUCT_DIV_SELECTOR)
        else:
            self.PRODUCT_DIV = (By.CSS_SELECTOR, settings.PRODUCT_DIV_SELECTOR)

        self.PRODUCT_URL = (By.CSS_SELECTOR, settings.PRODUCT_URL_SELECTOR)
        self.PRODUCT_TITLE = (By.CSS_SELECTOR, settings.PRODUCT_TITLE_SELECTOR)
        self.PRODUCT_PRICE = (By.CSS_SELECTOR, settings.PRODUCT_PRICE_SELECTOR)

    def close_initial_popup(self):
        if self.POPUP_CLOSE_BUTTON and self.POPUP_CLOSE_BUTTON[1]:
            self.close_popup(self.POPUP_CLOSE_BUTTON)
        else:
            print("Selector de pop-up no definido o vacío en .env, omitiendo cierre de pop-up.")

    def get_sort_dropdown_element(self):
        if not self.SORT_DROPDOWN or not self.SORT_DROPDOWN[1]:
            raise ValueError("El selector para el dropdown de ordenar no está configurado.")
        return self.find_element(self.SORT_DROPDOWN)

    def select_sort_option(self, option_text):
        from selenium.webdriver.support.ui import Select
        from selenium.webdriver.support import expected_conditions as EC

        try:
            element = self.find_element((By.XPATH, '//*[@id="topOfPage"]/div[6]/div/div[1]/main/div'))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

            sort_dropdown = self.get_sort_dropdown_element()
            time.sleep(1)

            self.driver.execute_script(
                "arguments[0].value = 'price'; arguments[0].dispatchEvent(new Event('change'));",
                sort_dropdown
            )

            select = Select(sort_dropdown)
            select.select_by_visible_text(option_text)

            self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_DIV))
            print(f"Productos ordenados por '{option_text}'.")
        except Exception as e:
            print(f"No se pudo ordenar los productos: {e}")

    def get_all_products_info(self):
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_DIV))
        product_elements = self.driver.find_elements(*self.PRODUCT_DIV)
        products_info = []
        for product in product_elements:
            print(product)
            try:
                title = product.find_element(*self.PRODUCT_TITLE).text
                url = product.find_element(*self.PRODUCT_TITLE).get_attribute("href")
                price_text = product.find_element(*self.PRODUCT_PRICE).text
                price = float(price_text.replace('$', '').replace(',', ''))
                products_info.append({"title": title, "url": url, "price": price})
            except Exception as e:
                print(f"Error al extraer información de un producto: {e}")
                continue
        return products_info