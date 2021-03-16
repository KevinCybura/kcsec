from decimal import Decimal
from typing import TYPE_CHECKING

from django import forms
from django.core import validators

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
    )
    price = forms.DecimalField(
        validators=[validators.MinValueValidator(0.0)],
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
        required=False,
        disabled=True,
    )
    cost = forms.DecimalField(widget=forms.HiddenInput(), required=False, disabled=True)
    filled = forms.BooleanField(widget=forms.HiddenInput(), required=False, disabled=True)

    class Meta:
        model = CryptoOrder
        fields = ("price", "shares", "portfolio", "symbol", "order_type", "trade_type", "filled")
        widgets = {
            "trade_type": forms.RadioSelect(
                attrs={"class": "btn-trade-type-radio btn btn-secondary", "type": "button"},
            ),
            "order_type": forms.Select(attrs={"class": "order-btn-select btn btn-secondary", "type": "button"}),
        }

    def clean_shares(self):
        shares = self.cleaned_data["shares"]
        if shares < Decimal("0.01"):
            self.add_error("shares", "Fractional shares cant be lower than 0.01")

        return shares

    def clean(self):
        cleaned_data = super().clean()

        trade_type = self.cleaned_data["trade_type"]
        order_type = self.cleaned_data["order_type"]
        portfolio = self.cleaned_data["portfolio"]
        shares = self.cleaned_data.get("shares")

        # If its a market order we just buy at the latest price.
        if order_type == CryptoOrder.OrderType.MARKET:
            cleaned_data["filled"] = True
            cleaned_data["price"] = round(
                Ohlcv.objects.filter(symbol=self.cleaned_data["symbol"], exchange="gemini", time_frame="1m")
                .latest()
                .close,
                ndigits=5,
            )
        else:
            cleaned_data["filled"] = False

        price = self.cleaned_data["price"]

        if shares:
            if trade_type == CryptoOrder.TradeType.SELL:
                share: "CryptoShareQuerySet" = portfolio.cryptoshare_set.filter(symbol=self.cleaned_data["symbol"])
                if share.exists() and shares > share[0].shares:
                    self.add_error("shares", "Not enough shares to sell.")

            # Populate cost field.
            cleaned_data["cost"] = shares * price

            if cleaned_data["cost"] > portfolio.balance:
                self.add_error("cost", "Not enough cash in account balance to fulfill order try using a limit order.")

        return cleaned_data

    def save(self, commit=True):
        order: CryptoOrder = super().save(commit=commit)
        # If the order has not yet been filled dont update anything.
        if order.filled:
            share, created = CryptoShare.objects.execute_order(order=order)

            # Delete the share row if there are no more shares
            if not created and share.shares == 0:
                share.delete()

            # Update portfolio cash balance.
            if order.trade_type == CryptoOrder.TradeType.SELL:
                order.portfolio.balance += order.shares * order.price
            else:
                order.portfolio.balance -= order.shares * order.price

            order.portfolio.save()

        return order
