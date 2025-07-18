from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from pages.brew_coffee_page import BrewCoffeePage
from pages.product_detail_page import ProductDetailPage
from config.settings import settings

def setup_driver():
    ua = UserAgent()

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument(f"user-agent={ua.random}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1920, 1080)
    return driver

def main():
    driver = setup_driver()
    try:
        brew_coffee_page = BrewCoffeePage(driver)
        brew_coffee_page.go_to_url(settings.BASE_URL)

        print("Intentando cerrar el pop-up si existe...")
        brew_coffee_page.close_initial_popup()

        if settings.SORT_DROPDOWN_SELECTOR and settings.SORT_OPTION_LOW_TO_HIGH_TEXT:
            print(f"Ordenando productos por precio (de menor a mayor) usando la opción: '{settings.SORT_OPTION_LOW_TO_HIGH_TEXT}'...")
            brew_coffee_page.select_sort_option(settings.SORT_OPTION_LOW_TO_HIGH_TEXT)
            print("Productos ordenados.")
        else:
            print("La configuración para ordenar por precio no está completa en .env. Saltando el ordenamiento.")

        all_products = brew_coffee_page.get_all_products_info()
        df_all_products = pd.DataFrame(all_products)
        df_all_products = df_all_products.sort_values(by="price").reset_index(drop=True)

        print("\n--- Todos los productos extraídos (ordenados por precio) ---")
        print(df_all_products.head())

        output_file_all = "outputs/all_coffee_equipment.csv"
        df_all_products.to_csv(output_file_all, index=False)
        print(f"\nTodos los productos guardados en '{output_file_all}'")

        top_5_cheapest = df_all_products.head(5)
        detailed_products_info = []

        product_detail_page = ProductDetailPage(driver)
        for index, product in top_5_cheapest.iterrows():
            print(f"\nExtrayendo detalles para: {product['title']} ({product['url']})")
            driver.get(product['url'])
            details = product_detail_page.get_product_details()
            combined_info = {**product.to_dict(), **details}
            detailed_products_info.append(combined_info)

        df_detailed_products = pd.DataFrame(detailed_products_info)
        output_file_detailed = "outputs/top_5_cheapest_detailed.csv"
        df_detailed_products.to_csv(output_file_detailed, index=False)
        print(f"\nInformación detallada de los 5 productos más baratos guardada en '{output_file_detailed}'")

        print("\n--- Proceso completado exitosamente ---")

    except ValueError as ve:
        print(f"Error de configuración: {ve}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        driver.quit()
        print("Navegador cerrado.")

if __name__ == "__main__":
    main()