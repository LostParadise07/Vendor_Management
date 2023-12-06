from django.contrib import admin
from .models import (PurchaseOrder, Vendor, HistoricalPerformance)


# Register your models here.

admin.site.register(PurchaseOrder)
admin.site.register(Vendor)
admin.site.register(HistoricalPerformance)
