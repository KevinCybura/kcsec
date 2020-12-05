from django import forms
from django.forms.utils import ErrorList

from kcsec.core.models import Portfolio
from kcsec.crypto.models import CryptoOrder
from kcsec.crypto.models import CryptoShare
from kcsec.crypto.models import Symbol


class OrderForm(forms.ModelForm):
    crypto_symbol = forms.ModelChoiceField(queryset=Symbol.objects.all(), widget=forms.HiddenInput())
    portfolio = forms.ModelChoiceField(queryset=Portfolio.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = CryptoOrder
        fields = ("price", "shares", "portfolio", "crypto_symbol", "order_type")
        widgets = {
            "price": forms.TextInput(attrs={"class": "order-control form-control form-control-sm order-price"}),
            "shares": forms.TextInput(attrs={"class": "order-control form-control form-control-sm"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, error_class=TableErrorList)

    def save(self, commit=True):
        self.instance.filled = True
        order: CryptoOrder = super().save(commit=commit)
        CryptoShare.objects.execute_order(order=self.instance)
        return order


class TableErrorList(ErrorList):
    def __str__(self):
        return self.as_table()

    def as_table(self):
        if not self:
            return ""
        return '<tr class="errorlist">%s</tr>' % "".join(['<tr class="error">%s</div>' % e for e in self])
