from django import forms
from django.core.validators import MinValueValidator
from django.forms.utils import ErrorList

from kcsec.core.models import Portfolio
from kcsec.crypto.models import CryptoOrder
from kcsec.crypto.models import CryptoShare
from kcsec.crypto.models import Ohlcv
from kcsec.crypto.models import Symbol


class OrderForm(forms.ModelForm):
    crypto_symbol = forms.ModelChoiceField(queryset=Symbol.objects.all(), widget=forms.HiddenInput())
    portfolio = forms.ModelChoiceField(queryset=Portfolio.objects.all(), widget=forms.HiddenInput())
    shares = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm", "placeholder": 0}),
        validators=[MinValueValidator(0.0)],
    )
    price = forms.DecimalField(
        validators=[MinValueValidator(0.0)],
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
        required=False,
        disabled=True,
    )

    class Meta:
        model = CryptoOrder
        fields = ("price", "shares", "portfolio", "crypto_symbol", "order_type", "trade_type")
        widgets = {
            "trade_type": forms.RadioSelect(
                attrs={"class": "btn-trade-type-radio btn btn-secondary", "type": "button"}
            ),
            "order_type": forms.Select(attrs={"class": "order-btn-select btn btn-secondary", "type": "button"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, error_class=TableErrorList)

    def save(self, commit=True):
        if self.cleaned_data["order_type"] == CryptoOrder.OrderType.MARKET:
            # If its a market order we just buy at the latest price eventually lets use an orderbook.
            self.instance.price = self.get_price()

        self.instance.filled = True
        order: CryptoOrder = super().save(commit=commit)
        CryptoShare.objects.execute_order(order=self.instance)
        return order

    def get_price(self):
        return Ohlcv.objects.latest_price(
            symbol=self.cleaned_data["crypto_symbol"],
            exchange="gemini",
            time_frame="1m",
        )


class TableErrorList(ErrorList):
    def __str__(self):
        return self.as_table()

    def as_table(self):
        if not self:
            return ""
        return '<tr class="errorlist">%s</tr>' % "".join(['<div class="error">%s</div>' % e for e in self])
