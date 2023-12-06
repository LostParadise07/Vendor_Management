from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="profile"),
    path("create_vendor", views.create_vendor, name="create_vendor"),
    path("list_vendors", views.list_vendors, name="list_vendors"),
    path("delete_vendor/<int:vendor_id>", views.delete_vendor, name="delete_vendor"),
    path("update_vendor/<int:vendor_id>", views.update_vendor, name="update_vendor"),
    path("create_purchase", views.create_purchase, name="create_purchase"),
    path("list_purchases", views.list_purchases, name="list_purchases"),
    path("delete_purchase/<int:purchase_id>", views.delete_purchase, name="delete_purchase"),
    path("update_purchase/<int:purchase_id>", views.update_purchase, name="update_purchase"),
    path("api/vendors/<int:vendor_id>/performance", views.get_vendor_performance, name="get_vendor_performance"),
    path("vendor_details/<int:vendor_id>", views.vendor_details, name="vendor_details"),
]
