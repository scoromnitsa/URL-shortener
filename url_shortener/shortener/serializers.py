from rest_framework import serializers
from .models import ShortURL
from django.utils import timezone
from datetime import timedelta

class ShortURLSerializer(serializers.ModelSerializer):
    last_hour_clicks = serializers.SerializerMethodField()
    last_day_clicks = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = ['id', 'short_code', 'orig_link', 'is_active', 'created_at', 'expires_at', 'last_hour_clicks', 'last_day_clicks']
        read_only_fields = ['short_code', 'created_at', 'expires_at']

    def get_last_hour_clicks(self, obj):
        return obj.clicks.filter(timestamp__gte=timezone.now() - timedelta(hours=1)).count()

    def get_last_day_clicks(self, obj):
        return obj.clicks.filter(timestamp__gte=timezone.now() - timedelta(days=1)).count()