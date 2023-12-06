import random
import string
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Vendor ,HistoricalPerformance,PurchaseOrder
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Avg, F

def index(request,message=None):
    context = {'segment': 'index'}
    if message is not None:
        context[message[0]] = message[1]
    html_template = loader.get_template('profile_management/index.html')
    return HttpResponse(html_template.render(context, request))

def create_vendor(request, message=None):
    context = {'segment': 'index'}

    if message is not None:
        context[message[0]] = message[1]

    if request.method == 'POST':
        
            name = request.POST.get('name')
            contact_details = request.POST.get('contact_details')
            address = request.POST.get('address')
            
            if not name:  
                return render(request, 'profile_management/createvendor.html', {'error': 'Name is required'})
            print('*********************')
            # Remove spaces and convert name to lowercase for consistency
            clean_name = name.replace(" ", "").lower()

            # Take the first 3 characters of the name (if available)
            name_part = clean_name[:3]

            # Generate a random sequence of 2 characters
            random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=11))

            # Concatenate the name part and the random part to form the vendor code
            vendor_code =name_part + random_part

            vendor = Vendor(name=name, contact_details=contact_details, address=address, vendor_code=vendor_code)
            vendor.save()
            return render(request, 'profile_management/index.html')  
        

    return render(request, 'profile_management/createvendor.html', context)


def list_vendors(request,message=None):
    context = {'segment': 'index'}
    if message is not None:
        context[message[0]] = message[1]
    vendors=Vendor.objects.all()
    context['vendors'] = vendors
    return render(request, 'profile_management/list_vendors.html', context)


def delete_vendor(request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
    vendor.delete()
    return redirect('list_vendors')


def update_vendor(request,vendor_id):
    vendor= Vendor.objects.get(id=vendor_id)
    context = {
       'segment': 'index',
       'vendor': vendor,
       'vendor_id': vendor.id,
       'name': vendor.name,
       'contact_details': vendor.contact_details,
       'address': vendor.address,
       'code':vendor.vendor_code,
       'delivery':vendor.on_time_delivery_rate,
       'rating':vendor.quality_rating_avg,
       'fulfillment_rate':vendor.fulfillment_rate,
       'average_response_time':vendor.average_response_time,
    }
    if request.method == 'POST':
        vendor.name = request.POST.get('name')
        vendor.contact_details = request.POST.get('contact_details')
        vendor.address = request.POST.get('address')
        vendor.on_time_delivery_rate = request.POST.get('on_time_delivery_rate')
        vendor.quality_rating_avg = request.POST.get('quality_rating_avg')
        vendor.average_response_time = request.POST.get('average_response_time')
        vendor.fulfillment_rate = request.POST.get('fulfillment_rate')
        vendor.save()
        return redirect('list_vendors')
    return render(request, 'profile_management/update_vendor.html', context)


def create_purchase(request):
    if request.method == 'POST':
        random_letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        random_numbers = ''.join(random.choices(string.digits, k=3))
        po_number = random_letters + random_numbers
        vendor_id = request.POST['vendor']
        vendor = Vendor.objects.get(id=vendor_id)
        order_date = request.POST['order_date']
        delivery_date = request.POST['delivery_date']
        items = request.POST['items']
        quantity = request.POST['quantity']
        status = request.POST['status']
        quality_rating = request.POST.get('quality_rating', None)
        issue_date = request.POST['issue_date']
        acknowledgment_date = request.POST.get('acknowledgment_date', None)

        # Create PurchaseOrder object
        PurchaseOrder.objects.create(
            po_number=po_number,
            vendor=vendor,
            order_date=order_date,
            delivery_date=delivery_date,
            items=items,
            quantity=quantity,
            status=status,
            quality_rating=quality_rating,
            issue_date=issue_date,
            acknowledgment_date=acknowledgment_date
        )
        
        return render(request, 'profile_management/index.html') 

    else:
        vendors = Vendor.objects.all()
        context = {'vendors': vendors}
        return render(request, 'order_tracking/create_purchase.html', context)
    
def list_purchases(request):
    purchases = PurchaseOrder.objects.all()
    vendor=Vendor.objects.all()
    context = {'purchases': purchases,
               'vendors':vendor}
    return render(request, 'order_tracking/list_purchases.html', context)


def delete_purchase(request, purchase_id):
    purchase = PurchaseOrder.objects.get(id=purchase_id)
    purchase.delete()
    return redirect('list_purchases')


def update_purchase(request, purchase_id):
    purchase = PurchaseOrder.objects.get(id=purchase_id)
    vendors = Vendor.objects.all()
    context = {
        'purchase': purchase,
        'vendors': vendors,
        'purchase_id': purchase.id,
        'po_number': purchase.po_number,
        'vendor': purchase.vendor,
        'order_date': purchase.order_date.strftime('%Y-%m-%dT%H:%M'),
        'delivery_date': purchase.delivery_date.strftime('%Y-%m-%dT%H:%M'),
        'items': purchase.items,
        'quantity': purchase.quantity,
        'status': purchase.status,
        'quality_rating': purchase.quality_rating,
        'issue_date': purchase.issue_date.strftime('%Y-%m-%dT%H:%M'),
        'acknowledgment_date': purchase.acknowledgment_date.strftime('%Y-%m-%dT%H:%M')
    }
    if request.method == 'POST':
        
        purchase.vendor = Vendor.objects.get(id=request.POST['vendor'])
        purchase.order_date = request.POST['order_date']
        purchase.delivery_date = request.POST['delivery_date']
        purchase.items = request.POST['items']
        purchase.quantity = request.POST['quantity']
        purchase.status = request.POST['status']
        purchase.quality_rating = request.POST.get('quality_rating', None)
        purchase.issue_date = request.POST['issue_date']
        purchase.acknowledgment_date = request.POST.get('acknowledgment_date', None)
        purchase.save()
        if purchase.status == 'completed':
            update_vendor_performance(purchase.vendor)
        return redirect('list_purchases')
    return render(request, 'order_tracking/update_purchase.html', context)


def update_vendor_performance(vendor):
    # Calculate on-time delivery rate
    completed_orders = PurchaseOrder.objects.filter(
        vendor=vendor, status='completed', delivery_date__lte=F('acknowledgment_date')
    ).count()
    total_completed_orders = PurchaseOrder.objects.filter(
        vendor=vendor, status='completed'
    ).count()
    on_time_delivery_rate = (completed_orders / total_completed_orders) * 100

    # Calculate quality rating average
    completed_orders_with_rating = PurchaseOrder.objects.filter(
        vendor=vendor, status='completed', quality_rating__isnull=False
    )
    quality_rating_avg = completed_orders_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']

    # Calculate average response time
    response_times = PurchaseOrder.objects.filter(
    vendor=vendor, acknowledgment_date__isnull=False
    ).aggregate(average_response_time=Avg(F('acknowledgment_date') - F('issue_date')))

    # Extract the average response time from the timedelta and convert it to seconds
    average_response_time_timedelta = response_times['average_response_time']
    average_response_time_seconds = average_response_time_timedelta.total_seconds()

    fulfilled_orders = PurchaseOrder.objects.filter(
        vendor=vendor, status='completed', acknowledgment_date__isnull=False
    ).count()
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfillment_rate = (fulfilled_orders / total_orders) * 100


    # Create or update HistoricalPerformance record
    HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=on_time_delivery_rate,
        quality_rating_avg=quality_rating_avg,
        average_response_time=average_response_time_seconds,  # Assign the converted value
        fulfillment_rate=fulfillment_rate
    )

def get_vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
        performance_metrics = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return render(request, 'performance_metrics.html', {'performance_metrics': performance_metrics})
    except Vendor.DoesNotExist:
        return render(request, 'error.html', {'message': 'Vendor not found'}, status=404)
    except Exception as e:
        return render(request, 'error.html', {'message': str(e)}, status=500)
    


def vendor_details(request, vendor_id):
    try:
        # Get the vendor
        vendor = Vendor.objects.get(id=vendor_id)
        
        # Get the vendor's purchase orders
        purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
        
        # Get the vendor's historical performance records
        historical_performance = HistoricalPerformance.objects.filter(vendor=vendor)
        
        # Prepare data to pass to the template
        context = {
            'vendor': vendor,
            'purchase_orders': purchase_orders,
            'historical_performance': historical_performance,
        }
        
        return render(request, 'profile_management/vendor_details.html', context)
    except Vendor.DoesNotExist:
        return render(request, 'error.html', {'message': 'Vendor not found'}, status=404)
    except Exception as e:
        return render(request, 'error.html', {'message': str(e)}, status=500)
