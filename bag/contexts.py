from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    # get bag session
    bag = request.session.get('bag', {})

    # for each idem id and the quantity in bag session
    for item_id, quantity in bag.items():
        #get the product
        product = get_object_or_404(Product, pk=item_id)
        # total is quantity times the price
        total += quantity * product.price
        # incremenet product count is quantity
        product_count += quantity
        # append the bag with each context
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    # id the total price is less than the free delivery price in settings
    if total < settings.FREE_DELIVERY_THRESHOLD:
        # delivery = total price times decimal percentage of delivery price
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        # delivery is total minus the threshold price
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        # else delivery is free
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context