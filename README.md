#  New York Taxi excel faylini PostgreSQL da ochish 

Ushbu loyiha NYC Taxi datasetidan foydalangan holda **Django REST API** orqali foydalanuvchiga hisobot taqdim etadi.  

---

## Maqsad  
- `.xlsx` formatdagi NYC taxi ma’lumotlarini PostgreSQL bazasiga yuklash  
- Safarlarni masofaga qarab toifalash va statistik hisobot yaratish  
- API orqali JSON formatida natija qaytarish  

---

##  Ma’lumotlarni PostgreSQL’ga import qilish

### 1. Excel faylni CSV formatiga aylantirish  
PostgreSQL `.xlsx` faylni to‘g‘ridan-to‘g‘ri qo‘llab-quvvatlamaydi, shuning uchun avval faylni `.csv` ga saqlaymiz.  

---

### 2. Jadval yaratish

```sql
CREATE TABLE nyc_taxi_trips (
    vendor_id TEXT,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count INTEGER,
    trip_distance FLOAT,
    pickup_longitude FLOAT,
    pickup_latitude FLOAT,
    rate_code INTEGER,
    store_and_fwd_flag TEXT,
    dropoff_longitude FLOAT,
    dropoff_latitude FLOAT,
    payment_type TEXT,
    fare_amount FLOAT,
    surcharge FLOAT,
    mta_tax FLOAT,
    tip_amount FLOAT,
    tolls_amount FLOAT,
    total_amount FLOAT
);
```

### 3. CSV fayldan ma’lumotlarni import qilish

```sql
COPY nyc_taxi_trips(
    vendor_id, pickup_datetime, dropoff_datetime, passenger_count, trip_distance, 
    pickup_longitude, pickup_latitude, rate_code, store_and_fwd_flag, 
    dropoff_longitude, dropoff_latitude, payment_type, fare_amount, surcharge, 
    mta_tax, tip_amount, tolls_amount, total_amount
)
FROM '~/Downloads/Telegram Desktop/new_york_taxi_1_mln.csv'
DELIMITER ','
CSV HEADER;

```
