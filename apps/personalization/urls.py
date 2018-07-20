from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


urlpatterns = [
    path('search/', views.SearchList.as_view(), name='search'),
    path('api/list/', login_required(views.ApiWishlistDetail.as_view()), name='wishlist-detail'),
    path('api/list/toggle/', login_required(views.ListToggle.as_view()), name='wishlist-toggle'),
]
