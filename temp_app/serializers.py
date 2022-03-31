from .models import book,Country
from rest_framework import serializers



class bookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.first_name')
    class Meta:
        model=book
        fields=['id','title','author','owner','relese_date']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model=Country
        fields="__all__"
