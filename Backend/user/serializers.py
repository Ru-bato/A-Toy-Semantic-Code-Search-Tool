from rest_framework import serializers

from .models import Favorite


# This is a serializer to deal with favorite recording
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'item_title', 'item_link', 'added_date']
