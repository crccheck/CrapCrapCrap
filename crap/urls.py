from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from apps.tracker.views import ReceiverView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('', include('apps.personalization.urls')),
    path('admin/', admin.site.urls),
    path('receive/', csrf_exempt(ReceiverView.as_view())),
]
