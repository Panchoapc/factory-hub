from django.contrib import admin
from django.urls import path
from sales_orders import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("clients/", urls.client_list, name="client-list"),
    path("clients/<int:pk>/", urls.client_detail, name="client-detail"),
    path("products/", urls.product_list, name="product-list"),
    path("products/<int:pk>/", urls.product_detail, name="product-detail"),
    path("salesorders/", urls.salesorder_list, name="salesorder-list"),
    path("salesorders/<int:pk>/", urls.salesorder_detail, name="salesorder-detail"),
]
