from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


urlpatterns = [
    path('api/list/toggle/', login_required(views.ListToggle.as_view()), name='list-toggle'),
]
