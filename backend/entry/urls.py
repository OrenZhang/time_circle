from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from utils import exceptions

urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url=f"{settings.SIMPLEUI_INDEX}/favicon.ico"),
    ),
    path("admin/", admin.site.urls)
]

handler400 = exceptions.bad_request
handler403 = exceptions.permission_denied
handler404 = exceptions.page_not_found
handler500 = exceptions.server_error
