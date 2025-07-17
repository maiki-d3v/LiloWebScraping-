from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from components.product_component import ProductComponent
import time


class ProductListingPage(BasePage):
    # Locators
    SORT_DROPDOWN = (By.ID, "ns-sort-dropdown")
    PRODUCTS_PER_PAGE_DROPDOWN = (By.CSS_SELECTOR, "select[name='ns-sort-dropdown']")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, "a.product")
    PAGINATION_INFO = (By.CLASS_NAME, "pagination-info")

    def __init__(self, driver):
        super().__init__(driver)

    def sort_products_by(self, sort_option="Price: Ascending"):
        """Sort products by given option"""
        self.select_dropdown_option(self.SORT_DROPDOWN, sort_option)
        time.sleep(2)  # Wait for page to reload

    def set_products_per_page(self, number=100):
        """Set number of products to display per page"""
        self.select_dropdown_option(self.PRODUCTS_PER_PAGE_DROPDOWN, str(number))
        time.sleep(2)  # Wait for page to reload

    def get_all_products(self):
        """Get all products on the current page"""
        products = []
        product_elements = self.get_elements(self.PRODUCT_ITEMS)

        for element in product_elements:
            products.append(ProductComponent(self.driver, element))

        return products

    def get_total_products_count(self):
        """Get total number of products from pagination info"""
        pagination_text = self.get_element_text(self.PAGINATION_INFO)
        # Example text: "0 - 12 of 194 items"
        try:
            return int(pagination_text.split("of")[1].split("items")[0].strip())
        except:
            return len(self.get_elements(self.PRODUCT_ITEMS))

    def go_to_next_page(self):
        """Navigate to next page if available"""
        next_buttons = self.driver.find_elements(By.CSS_SELECTOR, "a[aria-label='Next']")
        if next_buttons and "disabled" not in next_buttons[0].get_attribute("class"):
            next_buttons[0].click()
            time.sleep(2)  # Wait for page to load
            return True
        return False