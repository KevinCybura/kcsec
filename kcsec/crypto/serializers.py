from rest_framework import serializers


class ChartDataSerializer(serializers.Serializer):
    symbol = serializers.CharField(write_only=True)
    time = serializers.IntegerField(read_only=True)
    open = serializers.FloatField(read_only=True)
    high = serializers.FloatField(read_only=True)
    low = serializers.FloatField(read_only=True)
    close = serializers.FloatField(read_only=True)
    volume = serializers.FloatField(read_only=True)
    value = serializers.FloatField(read_only=True)

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        return super().update(validated_data)

    def create(self, validated_data):
        return super().create(validated_data)
