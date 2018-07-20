from django.urls import path

from . import views


urlpatterns = [
    path('api/list/toggle/', views.ListToggle.as_view(), name='list-toggle'),
]
