from django.shortcuts import render

from kcsec.crypto.forms import SomeForm

COINS = ["BTCUSD", "ETHUSD", "LTCUSD"]


# Create your views here.
def index(request):
    form = SomeForm()
    return render(request, "crypto/index.html", {"coins": COINS})
