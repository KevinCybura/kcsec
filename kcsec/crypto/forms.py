from typing import TYPE_CHECKING

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from kcsec.core.models import Portfolio
from kcsec.crypto.models import CryptoOrder
from kcsec.crypto.models import CryptoShare
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.models import Symbol

if TYPE_CHECKING:
    from kcsec.crypto.models.querysets.share import CryptoShareQuerySet


class OrderForm(forms.ModelForm):
    symbol = forms.ModelChoiceField(queryset=Symbol.objects.all(), widget=forms.HiddenInput(), required=True)
    portfolio = forms.ModelChoiceField(queryset=Portfolio.objects.all(), widget=forms.HiddenInput(), required=True)
    shares = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm", "placeholder": 0}),
        validators=[validators.MinValueValidator(0.0)],
    )
    price = forms.DecimalField(
        validators=[validators.MinValueValidator(0.0)],
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
        required=False,
        disabled=True,
    )

    class Meta:
        model = CryptoOrder
        fields = ("price", "shares", "portfolio", "symbol", "order_type", "trade_type")
        widgets = {
            "trade_type": forms.RadioSelect(
                attrs={"class": "btn-trade-type-radio btn btn-secondary", "type": "button"},
            ),
            "order_type": forms.Select(attrs={"class": "order-btn-select btn btn-secondary", "type": "button"}),
        }

    def clean_trade_type(self):
        trade_type = self.cleaned_data["trade_type"]
        if trade_type == CryptoOrder.TradeType.SELL:
            share: "CryptoShareQuerySet" = self.cleaned_data["portfolio"].cryptoshare_set.filter(
                symbol=self.cleaned_data["symbol"]
            )
            if share.exists() and self.cleaned_data["shares"] > share[0].shares:
                raise ValidationError("Not enough shares to sell.")

        return trade_type

    def save(self, commit=True):
        if self.cleaned_data["order_type"] == CryptoOrder.OrderType.MARKET:
            # If its a market order we just buy at the latest price eventually lets use an orderbook.
            latest = Ohlcv.objects.filter(
                symbol=self.cleaned_data["symbol"],
                exchange="gemini",
                time_frame="1m",
            ).latest()

            self.instance.price = latest.close

        self.instance.filled = True
        order: CryptoOrder = super().save(commit=commit)
        CryptoShare.objects.execute_order(order=self.instance)
        return order
