import django_filters


# Not using this DELETE?
class OhlcvFilter(django_filters.FilterSet):
    symbol = django_filters.CharFilter(field_name="symbol_id")
    asset_id_base = django_filters.CharFilter(field_name="asset_id_base")
    asset_id_quote = django_filters.CharFilter(field_name="asset_id_quote")
    exchange = django_filters.CharFilter(field_name="exchange")
    time_open = django_filters.DateTimeFromToRangeFilter()

    o = django_filters.OrderingFilter(fields=["time_open"])
    limit = django_filters.NumberFilter(method="limit_to", label="limit to n values")
    list = django_filters.NumberFilter(method="to_list", label="convert dict -> list")

    def limit_to(self, query_set, _field_name, value):
        if self.request.GET.get("o") == "time_open":
            qs = query_set.filter()
            value = qs.count() - value
            return qs[value:]
        return query_set.all()[:value]
