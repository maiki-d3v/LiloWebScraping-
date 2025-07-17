from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.product_listing_page import ProductListingPage
from pages.product_page import ProductPage
from utils.helpers import save_to_csv, create_timestamped_filename
from config.settings import settings
import time
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_driver():
    """Configure and return Selenium WebDriver"""
    options = webdriver.ChromeOptions()

    if settings.HEADLESS_MODE:
        options.add_argument("--headless")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(settings.IMPLICIT_WAIT)
    driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)

    return driver


def scrape_all_products(driver):
    """Scrape all products with their basic info"""
    logger.info("Iniciando scraping de productos...")
    driver.get(settings.BASE_URL)
    listing_page = ProductListingPage(driver)

    # Configurar página de listado
    logger.info(f"Configurando {settings.PRODUCTS_PER_PAGE} productos por página...")
    listing_page.set_products_per_page(settings.PRODUCTS_PER_PAGE)

    logger.info(f"Ordenando productos por: {settings.SORT_OPTION}")
    listing_page.sort_products_by(settings.SORT_OPTION)

    all_products = []
    processed_urls = set()
    product_count = 0

    while product_count < settings.MAX_PRODUCTS_TO_SCRAPE:
        products = listing_page.get_all_products()

        for product in products:
            if product.url not in processed_urls:
                all_products.append({
                    'title': product.title,
                    'price': product.price,
                    'price_float': product.price_float,
                    'url': product.url
                })
                processed_urls.add(product.url)
                product_count += 1

                if product_count >= settings.MAX_PRODUCTS_TO_SCRAPE:
                    break

        # Romper el bucle si no hay más páginas
        if not listing_page.go_to_next_page():
            break

        time.sleep(settings.DELAY_BETWEEN_REQUESTS)

    logger.info(f"Se encontraron {len(all_products)} productos")
    return all_products


def scrape_product_details(driver, products):
    """Scrape detailed info for top N cheapest products"""
    logger.info(f"Obteniendo detalles para los {settings.CHEAPEST_PRODUCTS_LIMIT} productos más baratos...")
    detailed_products = []
    product_page = ProductPage(driver)

    cheapest_products = sorted(products, key=lambda x: x['price_float'])[:settings.CHEAPEST_PRODUCTS_LIMIT]

    for product in cheapest_products:
        try:
            logger.info(f"Procesando: {product['title']}")
            driver.get(product['url'])
            time.sleep(settings.DELAY_BETWEEN_REQUESTS)

            details = product_page.get_product_details()
            detailed_products.append(details)
        except Exception as e:
            logger.error(f"Error procesando {product['url']}: {str(e)}")
            continue

    return detailed_products


def main():
    driver = None
    try:
        driver = setup_driver()

        # Paso 1: Scrapear todos los productos
        all_products = scrape_all_products(driver)

        # Guardar todos los productos
        all_products_file = create_timestamped_filename("all_products")
        save_to_csv(all_products, all_products_file, settings.OUTPUT_DIR)

        # Paso 2: Scrapear detalles de los productos más baratos
        detailed_products = scrape_product_details(driver, all_products)

        # Guardar productos detallados
        detailed_file = create_timestamped_filename("cheapest_products_details")
        save_to_csv(detailed_products, detailed_file, settings.OUTPUT_DIR)

        logger.info("\nScraping completado exitosamente!")
        logger.info(f"Total de productos encontrados: {len(all_products)}")
        logger.info(f"Información detallada recolectada para {len(detailed_products)} productos")

    except Exception as e:
        logger.error(f"\nOcurrió un error: {str(e)}", exc_info=True)
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()