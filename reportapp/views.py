from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count, Avg, Sum, Max, Q
from django.db.models.functions import Round 

from .models import TaxiTrip


class Report(APIView):
    def get(self, request):
        stats = TaxiTrip.objects.filter(trip_distance__gt=0).aggregate(
            short_trips=Count('trip_distance', filter=Q(trip_distance__lt=1)),
            medium_trips=Count('trip_distance', filter=Q(trip_distance__gte=1, trip_distance__lt=5)),
            long_trips=Count('trip_distance', filter=Q(trip_distance__gte=5, trip_distance__lt=10)),
            very_long_trips=Count('trip_distance', filter=Q(trip_distance__gte=10)),           
            avg_distance=Round(Avg('trip_distance'), 2), 
            max_distance=Max('trip_distance'),
            total_distance=Round(Sum('trip_distance'), 2) 
        )
        return Response(stats)
