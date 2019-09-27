from rest_framework import serializers

from .models import Area


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ('id', 'code', 'name')


class CitySerializer(serializers.ModelSerializer):
    children = AreaSerializer(many=True)

    class Meta:
        model = Area
        fields = ('id', 'code', 'name', 'children')


class ProvinceSerializer(serializers.ModelSerializer):
    children = AreaSerializer(many=True)

    class Meta:
        model = Area
        fields = ('id', 'code', 'name', 'children')