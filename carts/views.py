from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from .models import Cart, CartItem
from store.models import Product


# Create your views here.


def _cart_id(request):
    cart_data = request.session.session_key
    if not cart_data:
        cart_data = request.session.create()
    return cart_data


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart_data2 = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        cart_data2 = Cart.objects.create(
            cart_id=_cart_id(request)

        )
    cart_data2.save()

    try:
        cart_item = CartItem.objects.get(producto=product, cart=cart_data2)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist as e:
        cart_item = CartItem.objects.create(

            producto=product,
            quantity=1,
            cart=cart_data2

        )
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id):
    cart_remove = Cart.objects.get(cart_id=_cart_id(request))
    product_remove = get_object_or_404(Product, id=product_id)
    car_item_remove = CartItem.objects.get(producto=product_remove, cart=cart_remove)
    print(car_item_remove.quantity)
    if car_item_remove.quantity > 1:
        car_item_remove.quantity -= 1
        car_item_remove.save()
    else:
        car_item_remove.delete()

    return redirect('cart')


def remove_cart_item(request, product_id):
    cart_item_remove = Cart.objects.get(cart_id=_cart_id(request))
    product_item_remove = get_object_or_404(Product, id=product_id)
    cart_item_remove = CartItem.objects.get(producto=product_item_remove, cart=cart_item_remove)
    cart_item_remove.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart_2 = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart_2, is_active=True)
        for cart_items_ in cart_items:
            total += (cart_items_.producto.price * cart_items_.quantity)
            quantity += cart_items_.quantity
        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist as e:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total

    }
    return render(request, 'store/cart.html', context)
