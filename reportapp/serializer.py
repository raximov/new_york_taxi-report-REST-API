from rest_framework import serializers
from .models import TaxiTrip

class TaxiTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxiTrip
        fields = '__all__'
