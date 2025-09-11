from django.db import models

class TaxiTrip(models.Model):
    trip_distance = models.FloatField(db_index=True)
    category = models.PositiveSmallIntegerField(db_index=True)  # 1=short, 2=medium, 3=long, 4=very long

    class Meta:
        db_table = "taxi_trip"
