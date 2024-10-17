from rest_framework import serializers

from .models import Favorite, SearchRecord


# This is a serializer to deal with favorite recording
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'item_title', 'item_link', 'added_date']

class SearchRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchRecord
        fields = ['id', 'search_query', 'search_link','search_date']