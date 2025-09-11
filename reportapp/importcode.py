import os, sys
import django
from django.db import transaction
from openpyxl import load_workbook

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_york_taxi.settings")
django.setup()

from reportapp.models import TaxiTrip


def import_excel_efficiently(file_path):
    if not os.path.exists(file_path):
        print(f" Error '{file_path}' fayli topilmadi.")
        return

    print("Excel faylini o'qish...")

    try:
        workbook = load_workbook(filename=file_path, read_only=True)
        sheet = workbook.active

        batch_size = 100000
        records = []
        created = 0

        headers = [cell.value for cell in sheet[1]]  # header row
        trip_distance_idx = headers.index("trip_distance")  # index of distance column

        for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
            distance = row[trip_distance_idx]

            # Trip turini aniqlash
            if distance < 1:
                trip_type = 1
            elif distance < 5:
                trip_type = 2
            elif distance < 10:
                trip_type = 3
            else:
                trip_type = 4

            records.append(TaxiTrip(trip_distance=distance, category=trip_type))

            if len(records) >= batch_size:
                with transaction.atomic():
                    TaxiTrip.objects.bulk_create(records, batch_size)
                created += len(records)
                print(f"{created} ta row import qilindi...")
                records = []

        if records:
            with transaction.atomic():
                TaxiTrip.objects.bulk_create(records, batch_size)
            created += len(records)

        print(f" Import tugadi. Jami {created} ta row import qilindi.")

    except Exception as e:
        print(f"Importda error: {e}")


if __name__ == '__main__':
    excel_file_path = "/home/asus/Downloads/Telegram Desktop/new_york_taxi_1_mln.xlsx"
    import_excel_efficiently(excel_file_path)
