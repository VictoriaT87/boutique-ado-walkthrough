from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    # quantity is int number of string number from template
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # bag session, ends when window closes
    bag = request.session.get('bag', {})

    if size:
        # if the item has a size, add each size to quantity
        # separately in a dictionary
        if item_id in list(bag.keys()):
            # if the item is already in the bag,
            # and if same product id and size exists
            # add 1
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        # if there's no size,
        # item id is in bag session, add to quantity
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            # else quantity stays the same
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        # if item has a size
        if quantity > 0:
            # update quantity
            bag[item_id]['items_by_size'][size] = quantity
            # messages.success(request,
            #                  (f'Updated size {size.upper()} '
            #                   f'{product.name} quantity to '
            #                   f'{bag[item_id]["items_by_size"][size]}'))
        else:
            # delete with pop function
            del bag[item_id]['items_by_size'][size]
            # delete dictionary of sizes if nothing exists in it
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            # messages.success(request,
            #                  (f'Removed size {size.upper()} '
            #                   f'{product.name} from your bag'))
    else:
        # if item doesn't have a size
        if quantity > 0:
            # update quantity
            bag[item_id] = quantity
            # messages.success(request,
            #                  (f'Updated {product.name} '
            #                   f'quantity to {bag[item_id]}'))
        else:
            # delete item by pop function
            bag.pop(item_id)
            # messages.success(request,
            #                  (f'Removed {product.name} '
            #                   f'from your bag'))

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        # if item has a size
        if size:
            # remove that specific size
            del bag[item_id]['items_by_size'][size]
            # if the item_by_size dictionary is empty, delete completely
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        # successful redirect because it's a JS function
        return HttpResponse(status=200)

    # return 500 error if anything goes wrong
    except Exception as e:
        return HttpResponse(status=500)
