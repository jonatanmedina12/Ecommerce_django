from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from .models import Cart, CartItem
from store.models import Product, Variation


# Create your views here.


def _cart_id(request):
    cart_data = request.session.session_key
    if not cart_data:
        cart_data = request.session.create()
    return cart_data


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, Variation_category__iexact=key,
                                                  variation_value__iexact=value)
                product_variation.append(variation)
            except Exception as e:
                print(e)
                pass

    try:
        cart_data2 = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart_data2 = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart_data2.save()

    is_cart_item_exist = CartItem.objects.filter(producto=product, cart=cart_data2).exists()

    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(producto=product, cart=cart_data2)

        ex_var_list = []
        id_va = []

        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id_va.append(item.id)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id_va[index]
            item_update = CartItem.objects.get(producto=product, id=item_id)
            item_update.quantity += 1
            item_update.save()
        else:
            item_update = CartItem.objects.create(producto=product, quantity=1, cart=cart_data2)
            if len(product_variation) > 0:
                item_update.variations.clear()
                item_update.variations.add(*product_variation)
            item_update.save()
    else:
        cart_item = CartItem.objects.create(
            producto=product,
            quantity=1,
            cart=cart_data2
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id):
    try:
        cart_data2 = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        return redirect('cart')

    product = Product.objects.get(id=product_id)

    # Aquí usamos filter() en lugar de get()
    cart_items = CartItem.objects.filter(producto=product, cart=cart_data2)

    if cart_items.exists():
        for cart_item in cart_items:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

    return redirect('cart')


def remove_cart_item(request, product_id):
    cart_item_remove = Cart.objects.get(cart_id=_cart_id(request))
    product_item_remove = get_object_or_404(Product, id=product_id)
    cart_item_remove = CartItem.objects.get(producto=product_item_remove, cart=cart_item_remove)
    cart_item_remove.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
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
