from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.tracker.views import ReceiverView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('receive/', csrf_exempt(ReceiverView.as_view())),
]
