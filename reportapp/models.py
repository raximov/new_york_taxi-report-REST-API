from django.db import models

# Create your models here.

class TaxiTrip(models.Model):
    vendor_id = models.CharField(max_length=3)
    pickup_datetime = models.DateTimeField()
    dropoff_datetime = models.DateTimeField()
    passenger_count = models.IntegerField()
    trip_distance = models.FloatField()
    pickup_longitude = models.FloatField()
    pickup_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    payment_type = models.CharField(max_length=3)
    fare_amount = models.FloatField()
    surcharge = models.FloatField()
    mta_tax = models.FloatField()
    tip_amount = models.FloatField()
    tolls_amount = models.FloatField()
    total_amount = models.FloatField()

    class Meta:
        db_table = 'new_york_taxi' 