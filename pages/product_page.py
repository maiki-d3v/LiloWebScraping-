from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    # Locators
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.page-title")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "span.price--withoutTax")
    PRODUCT_UPC = (By.XPATH, "//th[contains(text(),'UPC')]/following-sibling::td")
    PRODUCT_SKU = (By.XPATH, "//th[contains(text(),'SKU')]/following-sibling::td")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, "img.gallery-placeholder__image")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, "div.product-description")

    def __init__(self, driver):
        super().__init__(driver)

    def get_product_details(self):
        """Extract all product details"""
        details = {
            'title': self.get_element_text(self.PRODUCT_TITLE),
            'price': self.get_element_text(self.PRODUCT_PRICE),
            'upc': self._get_detail(self.PRODUCT_UPC),
            'sku': self._get_detail(self.PRODUCT_SKU),
            'image_url': self._get_image_url(),
            'description': self._get_description()
        }
        return details

    def _get_detail(self, locator):
        """Helper method to get detail or return N/A if not found"""
        try:
            return self.get_element_text(locator)
        except:
            return "N/A"

    def _get_image_url(self):
        """Get product image URL"""
        try:
            return self.get_element(self.PRODUCT_IMAGE).get_attribute("src")
        except:
            return "N/A"

    def _get_description(self):
        """Get product description (limited to 500 chars)"""
        try:
            full_text = self.get_element_text(self.PRODUCT_DESCRIPTION)
            return (full_text[:497] + "...") if len(full_text) > 500 else full_text
        except:
            return "N/A"