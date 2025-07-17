import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Configuración de la aplicación
    BASE_URL = os.getenv('BASE_URL', 'https://prima-coffee.com/brew/coffee')
    MAX_PRODUCTS_TO_SCRAPE = int(os.getenv('MAX_PRODUCTS_TO_SCRAPE', '1000'))
    CHEAPEST_PRODUCTS_LIMIT = int(os.getenv('CHEAPEST_PRODUCTS_LIMIT', '5'))
    PRODUCTS_PER_PAGE = int(os.getenv('PRODUCTS_PER_PAGE', '100'))
    SORT_OPTION = os.getenv('SORT_OPTION', 'Price: Ascending')

    # Configuración de Selenium
    HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'true').lower() == 'true'
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    DELAY_BETWEEN_REQUESTS = float(os.getenv('DELAY_BETWEEN_REQUESTS', '2'))

    # Configuración de salida
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'outputs')

    @classmethod
    def get_output_path(cls, filename):
        """Obtiene la ruta completa del archivo de salida"""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        return os.path.join(cls.OUTPUT_DIR, filename)


# Instancia de configuración
settings = Settings()