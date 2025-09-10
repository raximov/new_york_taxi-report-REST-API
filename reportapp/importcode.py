import os, sys
import django
from django.db import transaction
from openpyxl import load_workbook

# Manually add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_york_taxi.settings")
django.setup()

from reportapp.models import TaxiTrip

def import_excel_efficiently(file_path):
    """
    Imports a large Excel file into the Django TaxiTrip model using openpyxl.
    This method is memory-efficient by processing data row by row.

    Args:
        file_path (str): The path to the XLSX file.
    """
    if not os.path.exists(file_path):
        print(f" Xatolik: '{file_path}' fayli topilmadi.")
        return

    print("Excel faylini o'qish...")
    
    try:
        workbook = load_workbook(filename=file_path, read_only=True)
        sheet = workbook.active  
        
        batch_size = 100000
        records = []
        headers = [cell.value for cell in sheet[1]]  # Read header row
        
        # Iterate over the rows, skipping the header
        for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
            row_dict = dict(zip(headers, row))
            
            records.append(TaxiTrip(
                vendor_id=row_dict.get('vendor_id'),
                pickup_datetime=row_dict.get('pickup_datetime'),
                dropoff_datetime=row_dict.get('dropoff_datetime'),
                passenger_count=row_dict.get('passenger_count'),
                trip_distance=row_dict.get('trip_distance'),
                pickup_longitude=row_dict.get('pickup_longitude'),
                pickup_latitude=row_dict.get('pickup_latitude'),
                rate_code=row_dict.get('rate_code'),
                store_and_fwd_flag=row_dict.get('store_and_fwd_flag'),
                dropoff_longitude=row_dict.get('dropoff_longitude'),
                dropoff_latitude=row_dict.get('dropoff_latitude'),
                payment_type=row_dict.get('payment_type'),
                fare_amount=row_dict.get('fare_amount'),
                surcharge=row_dict.get('surcharge'),
                mta_tax=row_dict.get('mta_tax'),
                tip_amount=row_dict.get('tip_amount'),
                tolls_amount=row_dict.get('tolls_amount'),
                total_amount=row_dict.get('total_amount'),
            ))
            
            if (i + 1) % batch_size == 0:
                with transaction.atomic():
                    TaxiTrip.objects.bulk_create(records, batch_size)
                print(f"{i + 1} ta row...")
                records = [] 

        if records:
            with transaction.atomic():
                TaxiTrip.objects.bulk_create(records, batch_size)
            print(f"Import tugadi Jami {i + 1} ta row import qilindi.")

    except Exception as e:
        print(f"Importda error: {e}")
        return

if __name__ == '__main__':
    excel_file_path = "/home/asus/Downloads/Telegram Desktop/new_york_taxi_1_mln.xlsx"
    import_excel_efficiently(excel_file_path)

