from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import User

from products.models import Product
from orders.models import Order


@login_required
def admin_panel(request):

    if request.user.role != 'admin':
        return redirect('/dashboard/')

    context = {
        'users_count': User.objects.count(),
        'products_count': Product.objects.count(),
        'orders_count': Order.objects.count(),
    }

    return render(
        request,
        'accounts/admin_panel.html',
        context
    )


@login_required
def users_list(request):

    if request.user.role != 'admin':
        return redirect('/dashboard/')

    users = User.objects.all().order_by('id')

    return render(
        request,
        'accounts/users_list.html',
        {
            'users': users
        }
    )


@login_required
def change_user_role(request, user_id):

    if request.user.role != 'admin':
        return redirect('/dashboard/')

    user = get_object_or_404(
        User,
        id=user_id
    )

    new_role = request.POST.get('role')

    if new_role in [
        'admin',
        'company',
        'sales'
    ]:
        user.role = new_role
        user.save()

    return redirect('/admin-users/')


@login_required
def delete_user(request, user_id):

    if request.user.role != 'admin':
        return redirect('/dashboard/')

    user = get_object_or_404(
        User,
        id=user_id
    )

    if user.id != request.user.id:
        user.delete()

    return redirect('/admin-users/')


@login_required
def admin_products(request):

    if request.user.role != 'admin':
        return redirect('/dashboard/')

    products = Product.objects.select_related(
        'company',
        'category'
    ).all().order_by('-id')

    return render(
        request,
        'accounts/admin_products.html',
        {
            'products': products
        }
    )


@login_required
def admin_delete_product(request, product_id):

    if request.user.role != 'admin':
        return redirect('/dashboard/')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    product.delete()

    return redirect('/admin-products/')