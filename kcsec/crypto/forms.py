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
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm"}), validators=[MinValueValidator(0.0)]
    )
    price = forms.DecimalField(
        validators=[MinValueValidator(0.0)],
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm", "step": "0.01"}),
        required=False,
        disabled=True,
    )

    class Meta:
        model = CryptoOrder
        fields = ("price", "shares", "portfolio", "crypto_symbol", "order_type", "trade_type")
        widgets = {
            "shares": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "trade_type": forms.RadioSelect(
                attrs={"class": "btn-trade-type-radio btn btn-secondary", "type": "button"}
            ),
            "order_type": forms.Select(attrs={"class": "order-btn-select btn btn-secondary", "type": "button"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, error_class=TableErrorList)

    def save(self, commit=True):
        if self.cleaned_data["order_type"] == CryptoOrder.OrderType.MARKET:
            self.instance.price = self.get_price()[0]

        self.instance.filled = True
        order: CryptoOrder = super().save(commit=commit)
        CryptoShare.objects.execute_order(order=self.instance)
        return order

    def get_price(self):
        return Ohlcv.objects.filter(
            asset_id_base=self.cleaned_data["crypto_symbol"].pk, exchange_id="gemini"
        ).values_list("close")[0]


class TableErrorList(ErrorList):
    def __str__(self):
        return self.as_table()

    def as_table(self):
        if not self:
            return ""
        return '<tr class="errorlist">%s</tr>' % "".join(['<div class="error">%s</div>' % e for e in self])
