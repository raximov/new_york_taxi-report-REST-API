from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count, Sum, Max, Q
from django.db.models.functions import Round

from .models import TaxiTrip


class Report(APIView):
    def get(self, request):
        stats = TaxiTrip.objects.filter(trip_distance__gt=0).only("trip_distance").aggregate(
            short_trips=Count("trip_distance", filter=Q(trip_distance__lt=1)),
            medium_trips=Count("trip_distance", filter=Q(trip_distance__gte=1, trip_distance__lt=5)),
            long_trips=Count("trip_distance", filter=Q(trip_distance__gte=5, trip_distance__lt=10)),
            very_long_trips=Count("trip_distance", filter=Q(trip_distance__gte=10)),
            max_distance=Max("trip_distance"),
            total_distance=Round(Sum("trip_distance"), 2),
        )

        stats["avg_distance"] = (round(stats["total_distance"] / (stats["short_trips"]
                                                                + stats["medium_trips"]
                                                                + stats["long_trips"]
                                                                + stats["very_long_trips"]
                                                            ), 2))
 
        return Response(stats)


class ReportSQL(APIView):
    def get(self, request):
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("""
                WITH statdata AS (
                    SELECT 
                        COUNT(CASE WHEN trip_distance < 1 THEN 1 END) AS short_trips,
                        COUNT(CASE WHEN trip_distance >= 1 AND trip_distance < 5 THEN 1 END) AS medium_trips,
                        COUNT(CASE WHEN trip_distance >= 5 AND trip_distance < 10 THEN 1 END) AS long_trips,
                        COUNT(CASE WHEN trip_distance >= 10 THEN 1 END) AS very_long_trips,
                        MAX(trip_distance) AS max_distance,
                        ROUND(SUM(trip_distance)::numeric, 2) AS total_distance
                    FROM taxi_trips
                    WHERE trip_distance > 0
                )
                SELECT COALESCE(json_agg(statdata), '[]'::json)
                FROM statdata;
            """)
            stats= cursor.fetchone()[0][0]

     
        total_trips = stats["short_trips"] + stats["medium_trips"] + stats["long_trips"] + stats["very_long_trips"]
        stats["avg_distance"] = round(stats["total_distance"] / total_trips, 2)
     

        return Response(stats)
