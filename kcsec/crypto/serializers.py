import locale
from datetime import datetime
from typing import TYPE_CHECKING

from django.forms.models import model_to_dict
from django.utils.timezone import utc
from rest_framework import serializers

from kcsec.crypto.models import CryptoShare
from kcsec.crypto.models import Ohlcv

if TYPE_CHECKING:
    from kcsec.crypto.models.querysets.share import CryptoShareQuerySet


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


class CryptoTemplateContext(serializers.Serializer):
    symbol = serializers.CharField()
    price = serializers.FloatField()
    formatted_price = serializers.SerializerMethodField()
    midnight_price = serializers.FloatField()
    percent_change = serializers.SerializerMethodField()
    price_change = serializers.SerializerMethodField()
    share_data = serializers.SerializerMethodField()
    order_data = serializers.SerializerMethodField(required=False)
    form = serializers.SerializerMethodField(required=False)

    @staticmethod
    def get_formatted_price(obj):
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        return locale.currency(obj["price"], grouping=True)

    @staticmethod
    def get_order_data(obj):
        if not obj["user"].is_authenticated or obj.get("update", False):
            return {}

        return list(
            obj["user"]
            .portfolio.cryptoorder_set.filter(symbol_id=obj["symbol"])
            .order_by("-created_at")
            .values("symbol_id", "shares", "price", "order_type", "trade_type", "created_at")[:5]
        )

    def get_share_data(self, obj):
        if not obj["user"].is_authenticated:
            return {}

        share: "CryptoShareQuerySet" = obj["user"].portfolio.cryptoshare_set.filter(symbol=obj["symbol"])

        # User doesnt have any shares of this symbol.
        if not share.exists():
            return None

        share: "CryptoShare" = share[0]

        equity = obj["price"] * share.shares

        total_price = (obj["price"] - share.average_price) * share.shares
        total_percent = share.average_percent_change(obj["price"])

        todays_price = (obj["price"] - obj["midnight_price"]) * share.shares
        todays_percent = self.get_percent_change(obj)

        # If the share row was created today set todays price/percent change to change since purchase
        midnight = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=utc)
        if share.created_at > midnight:
            todays_price = total_price
            todays_percent = total_percent

        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        model = model_to_dict(share)
        model["average_price"] = locale.currency(model["average_price"], grouping=True)
        return {
            "total_price": locale.currency(total_price, grouping=True),
            "total_percent": total_percent,
            "todays_price": locale.currency(todays_price, grouping=True),
            "todays_percent": todays_percent,
            "equity": locale.currency(equity, grouping=True),
            **model,
        }

    @staticmethod
    def get_percent_change(obj):
        return CryptoShare.percent_change(obj["price"], obj["midnight_price"])

    @staticmethod
    def get_price_change(obj):
        return locale.currency(obj["price"] - obj["midnight_price"], grouping=True)

    @staticmethod
    def get_form(obj):
        if invalid_form := obj.get("invalid_form"):
            return invalid_form
        if form_class := obj.get("form_class"):
            return form_class(
                initial={
                    "portfolio": getattr(obj["user"], "portfolio", None),
                    "symbol": obj["symbol"],
                    "price": round(obj["price"], 2),
                },
                auto_id=f"id_{obj['symbol']}_%s",
            )
