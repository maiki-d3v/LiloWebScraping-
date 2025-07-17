import csv
import os
from datetime import datetime
import logging


def save_to_csv(data, filename, output_dir):
    """Save data to CSV file"""
    try:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            if not data:
                logging.warning("No data to save to CSV")
                return

            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        logging.info(f"Datos guardados en {filepath}")
        return filepath
    except Exception as e:
        logging.error(f"Error al guardar CSV: {str(e)}")
        raise


def create_timestamped_filename(base_name, extension="csv"):
    """Create a filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"