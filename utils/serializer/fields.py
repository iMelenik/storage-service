from datetime import datetime

from rest_framework import serializers


class IntToDateTimeField(serializers.IntegerField):
    def to_internal_value(self, data):
        return datetime.fromtimestamp(float(data) / 1000) if data else None

    def to_representation(self, value):
        if not value:
            return None
        return int(value.timestamp() * 1000)
