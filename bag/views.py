from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    # quantity is int number of string number from template
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # bag session, ends when window closes
    bag = request.session.get('bag', {})

    # if item id is in bag session, add to quantity
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    # else quantity stays the same
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)