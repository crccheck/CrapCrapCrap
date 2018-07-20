from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


urlpatterns = [
    path('api/list/', login_required(views.WishlistDetail.as_view()), name='wishlist-detail'),
    path('api/list/toggle/', login_required(views.ListToggle.as_view()), name='wishlist-toggle'),
]
