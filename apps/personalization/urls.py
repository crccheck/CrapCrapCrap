from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


urlpatterns = [
    path('accounts/logout/', views.Logout.as_view(), name='logout'),
    path('accounts/profile/', views.Profile.as_view(), name='profile'),
    path('search/', views.SearchList.as_view(), name='search'),
    path('wishlist/', login_required(views.WishlistDetail.as_view()), name='wishlist'),
    path('api/list/', login_required(views.ApiWishlistDetail.as_view()), name='wishlist-detail'),
    path('api/list/toggle/', login_required(views.ListToggle.as_view()), name='wishlist-toggle'),
]
