from django.conf import settings
from django.urls import include
from django.urls import path

from kcsec.core import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.UserAuthView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
