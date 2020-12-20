import django_filters
from rest_framework import serializers

from kcsec.crypto.models import Ohlcv


class OhlcvSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(write_only=True)
    value = serializers.FloatField(read_only=True)
    time = serializers.FloatField(read_only=True)

    class Meta:
        model = Ohlcv
        fields = [
            "symbol",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "value",
            "time",
            "time_open",
            "asset_id_base",
            "asset_id_quote",
            "exchange",
        ]
        write_only_fields = ["symbol"]
        read_only_fields = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "value",
            "time",
            "time_open",
            "asset_id_base",
            "asset_id_quote",
            "exchange",
        ]


class OhlcvFilter(django_filters.FilterSet):
    asset_id_base = django_filters.CharFilter(field_name="asset_id_base")
    asset_id_quote = django_filters.CharFilter(field_name="asset_id_quote")
    exchange = django_filters.CharFilter(field_name="exchange")
    time_open = django_filters.DateTimeFromToRangeFilter()

    o = django_filters.OrderingFilter(fields=["time_open"])
    limit = django_filters.NumberFilter(method="limit_to", label="limit to n values")
    list = django_filters.NumberFilter(method="to_list", label="convert dict -> list")

    def limit_to(self, query_set, field_name, value):
        if self.request.GET.get("o") == "time_open":
            qs = query_set.filter()
            return qs[qs.count() - value :]
        return query_set.all()[:value]
