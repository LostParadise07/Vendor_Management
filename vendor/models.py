from django.db import models

class Vendor(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=100, unique=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO: {self.po_number} - Vendor: {self.vendor.name}"
    
    def update_on_time_delivery_rate(self):
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor, status='completed', delivery_date__lte=self.delivery_date
        ).count()
        total_completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor, status='completed'
        ).count()

        self.vendor.on_time_delivery_rate = (completed_orders / total_completed_orders) * 100
        self.vendor.save()

    def update_quality_rating_average(self, quality_rating):
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor, status='completed', quality_rating__isnull=False
        )
        average_rating = completed_orders.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
        self.vendor.quality_rating_avg = average_rating
        self.vendor.save()

    def update_average_response_time(self):
        response_times = PurchaseOrder.objects.filter(
            vendor=self.vendor, acknowledgment_date__isnull=False
        ).aggregate(average_response_time=Avg(F('acknowledgment_date') - F('issue_date')))
        
        self.vendor.average_response_time = response_times['average_response_time']
        self.vendor.save()

    def update_fulfillment_rate(self):
        fulfilled_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor, status='completed', acknowledgment_date__isnull=False
        ).count()
        total_orders = PurchaseOrder.objects.filter(vendor=self.vendor).count()

        self.vendor.fulfillment_rate = (fulfilled_orders / total_orders) * 100
        self.vendor.save()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
