from django.shortcuts import redirect, render
from products.models import Product


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('/cart/')


def cart_view(request):
    cart = request.session.get('cart', {})

    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'cart/cart.html', {
        'items': items,
        'total': total,
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('/cart/')

from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem


@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('/cart/')

    order = Order.objects.create(
        customer=request.user,
        total=0
    )

    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity
        total += subtotal

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

    order.total = total
    order.save()

    # Очищаем корзину
    request.session['cart'] = {}

    return render(request, 'cart/checkout_success.html', {
        'order': order
    })