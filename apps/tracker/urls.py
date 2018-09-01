from django.urls import path

from . import views


urlpatterns = [
    path('<slug:property_slug>/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
]
