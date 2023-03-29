from rest_framework.serializers import ModelSerializer
from .models import *


class CensusSerializer(ModelSerializer):
    
    class Meta:
        model = Census
        fields = '__all__'