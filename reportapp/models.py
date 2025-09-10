from django.db import models

class TaxiTrip(models.Model):
    vendor_id = models.CharField(max_length=3)
    pickup_datetime = models.DateTimeField()
    dropoff_datetime = models.DateTimeField()
    passenger_count = models.PositiveIntegerField()
    trip_distance = models.FloatField(db_index=True)
    pickup_longitude = models.FloatField(null=True, blank=True)
    pickup_latitude = models.FloatField(null=True, blank=True)
    dropoff_longitude = models.FloatField(null=True, blank=True)
    dropoff_latitude = models.FloatField(null=True, blank=True)
    rate_code = models.PositiveSmallIntegerField()
    store_and_fwd_flag = models.CharField(max_length=1, null=True, blank=True)
    payment_type = models.CharField(max_length=3)
    fare_amount = models.FloatField()
    surcharge = models.FloatField()
    mta_tax = models.FloatField()
    tip_amount = models.FloatField()
    tolls_amount = models.FloatField()
    total_amount = models.FloatField()

    class Meta:
        db_table = "taxi_trips"
        indexes = [
            models.Index(fields=["trip_distance"]),
        ]

