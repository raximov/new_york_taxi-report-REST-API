from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count, Sum, Max, Q
from django.db.models.functions import Round

from .models import TaxiTrip

class Report(APIView):
    def get(self, request):
        stats = TaxiTrip.objects.aggregate(
            short_trips=Count('id', filter=Q(category=1)),
            medium_trips=Count('id', filter=Q(category=2)),
            long_trips=Count('id', filter=Q(category=3)),
            very_long_trips=Count('id', filter=Q(category=4)),
            max_distance=Max('trip_distance'),
            total_distance=Round(Sum('trip_distance'),2)
        )

        stats["avg_distance"] = (round(stats["total_distance"] / (stats["short_trips"]
                                                                + stats["medium_trips"]
                                                                + stats["long_trips"]
                                                                + stats["very_long_trips"]
                                                            ), 2))
 
        return Response(stats)
