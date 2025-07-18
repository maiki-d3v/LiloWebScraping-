from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config.settings import settings


class ProductDetailPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.productView-title")
        self.PRODUCT_PRICE = (By.CSS_SELECTOR, "div.productView-price span.price.price--withoutTax")

        self.PRODUCT_SKU = (By.XPATH, settings.PRODUCT_SKU_SELECTOR)
        self.PRODUCT_UPC = (By.XPATH, settings.PRODUCT_UPC_SELECTOR)

        self.IMAGE_CAROUSEL_CONTAINER = (By.CSS_SELECTOR, "ul.productView-imageCarousel-main")

        self.CAROUSEL_IMAGE_LINK = (By.CSS_SELECTOR, "li.productView-imageCarousel-main-item a[href*='bigcommerce.com/s']")

    def get_product_details(self):
        details = {}
        try:
            self.wait.until(EC.presence_of_element_located(self.PRODUCT_TITLE))
            self.wait.until(EC.presence_of_element_located(self.PRODUCT_PRICE))

            details['title'] = self.driver.find_element(*self.PRODUCT_TITLE).text
            details['price'] = float(
                self.driver.find_element(*self.PRODUCT_PRICE).text.replace('$', '').replace(',', '').strip())

            try:
                sku_element = self.wait.until(EC.presence_of_element_located(self.PRODUCT_SKU))
                details['sku'] = sku_element.text.strip()
                print(f"Extracted SKU: {details['sku']}")
            except Exception as e:
                details['sku'] = "N/A"
                print(f"Could not extract SKU: {e}")

            try:
                upc_element = self.wait.until(EC.presence_of_element_located(self.PRODUCT_UPC))
                details['upc'] = upc_element.text.strip()
                print(f"Extracted UPC: {details['upc']}")
            except Exception as e:
                details['upc'] = "N/A"
                print(f"Could not extract UPC: {e}")

            details['image_urls'] = self.get_all_image_urls()
        except Exception as e:
            print(f"Error getting product details: {e}")
            raise
        return details

    def get_all_image_urls(self):
        image_urls = []
        try:
            self.wait.until(EC.presence_of_element_located(self.IMAGE_CAROUSEL_CONTAINER))

            image_link_elements = self.driver.find_elements(*self.CAROUSEL_IMAGE_LINK)

            if not image_link_elements:
                print("No image links found in the carousel.")
                return []

            for link_element in image_link_elements:
                href = link_element.get_attribute("href")
                if href:
                    image_urls.append(href)
            print(f"Found {len(image_urls)} image URLs.")

        except Exception as e:
            print(f"Error extracting image URLs from carousel: {e}")
        return image_urls