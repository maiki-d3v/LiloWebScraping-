import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()

        self.BASE_URL = os.getenv("BASE_URL")
        if not self.BASE_URL:
            raise ValueError("BASE_URL no está definida en el archivo .env")

        self.POPUP_CLOSE_BUTTON_SELECTOR = os.getenv("POPUP_CLOSE_BUTTON_SELECTOR")

        self.SORT_DROPDOWN_SELECTOR = os.getenv("SORT_DROPDOWN_SELECTOR")
        if not self.SORT_DROPDOWN_SELECTOR:
            print("Advertencia: SORT_DROPDOWN_SELECTOR no está definido. El ordenamiento no se realizará.")
            self.SORT_DROPDOWN_SELECTOR = None

        self.SORT_OPTION_LOW_TO_HIGH_TEXT = os.getenv("SORT_OPTION_LOW_TO_HIGH_TEXT")
        if not self.SORT_OPTION_LOW_TO_HIGH_TEXT and self.SORT_DROPDOWN_SELECTOR:
            print("Advertencia: SORT_OPTION_LOW_TO_HIGH_TEXT no está definida. El ordenamiento no se realizará.")
            self.SORT_OPTION_LOW_TO_HIGH_TEXT = None

        self.LIMIT_DROPDOWN_SELECTOR = os.getenv("LIMIT_DROPDOWN_SELECTOR")
        if not self.LIMIT_DROPDOWN_SELECTOR:
            print("Advertencia: LIMIT_DROPDOWN_SELECTOR no está definido. El ordenamiento no se realizará.")
            self.LIMIT_DROPDOWN_SELECTOR = None

        self.LIMIT_OPTION_100_TEXT = os.getenv("LIMIT_OPTION_100_TEXT")
        if not self.LIMIT_OPTION_100_TEXT and self.LIMIT_OPTION_100_TEXT:
            print("Advertencia: LIMIT_OPTION_100_TEXT no está definida. El ordenamiento no se realizará.")
            self.LIMIT_OPTION_100_TEXT = None

        self.PRODUCT_DIV_SELECTOR = os.getenv("PRODUCT_DIV_SELECTOR")
        if not self.PRODUCT_DIV_SELECTOR:
            raise ValueError("PRODUCT_DIV_SELECTOR no está definida en el archivo .env")

        self.PRODUCT_URL_SELECTOR = os.getenv("PRODUCT_URL_SELECTOR")
        if not self.PRODUCT_URL_SELECTOR:
            raise ValueError("PRODUCT_URL_SELECTOR no está definida en el archivo .env")

        self.PRODUCT_TITLE_SELECTOR = os.getenv("PRODUCT_TITLE_SELECTOR")
        if not self.PRODUCT_TITLE_SELECTOR:
            raise ValueError("PRODUCT_TITLE_SELECTOR no está definida en el archivo .env")

        self.PRODUCT_PRICE_SELECTOR = os.getenv("PRODUCT_PRICE_SELECTOR")
        if not self.PRODUCT_PRICE_SELECTOR:
            raise ValueError("PRODUCT_PRICE_SELECTOR no está definida en el archivo .env")

        self.PRODUCT_IMAGE_SELECTOR = os.getenv("PRODUCT_IMAGE_SELECTOR", "div.product-media__item img")
        self.PRODUCT_SKU_SELECTOR = os.getenv("PRODUCT_SKU_SELECTOR", "//strong[contains(text(), 'SKU:')]/following-sibling::span")
        self.PRODUCT_UPC_SELECTOR = os.getenv("PRODUCT_UPC_SELECTOR", "//strong[contains(text(), 'UPC:')]/following-sibling::span")

settings = Settings()