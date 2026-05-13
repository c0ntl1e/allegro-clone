from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Order, OrderItem
from products.models import Product


@login_required
def create_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('/cart/')

    total = 0

    # Создаём заказ
    order = Order.objects.create(
        customer=request.user,
        status='new',
        total=0
    )

    # Создаём позиции заказа
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

    # Обновляем сумму заказа
    order.total = total
    order.save()

    # Очищаем корзину
    request.session['cart'] = {}
    request.session.modified = True

    return render(request, 'orders/checkout_success.html', {
        'order': order
    })


@login_required
def company_orders(request):
    if request.user.role not in ['company', 'sales']:
        return redirect('/dashboard/')

    if request.user.role == 'company':
        company = request.user.owned_company
    else:
        company = request.user.company

    orders = Order.objects.filter(
        items__product__company=company
    ).distinct().order_by('-created_at')

    return render(request, 'orders/company_orders.html', {
        'orders': orders
    })


@login_required
def order_detail(request, pk):
    if request.user.role not in ['company', 'sales']:
        return redirect('/dashboard/')

    if request.user.role == 'company':
        company = request.user.owned_company
    else:
        company = request.user.company

    order = get_object_or_404(
        Order.objects.filter(
            items__product__company=company
        ).distinct(),
        pk=pk
    )

    items = order.items.filter(
        product__company=company
    ).select_related('product')

    if request.method == 'POST':
        status = request.POST.get('status')

        valid_statuses = [
            'new',
            'processing',
            'shipped',
            'completed',
            'cancelled',
        ]

        if status in valid_statuses:
            order.status = status
            order.save()

            return redirect(f'/company-orders/{order.id}/')

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
    })