from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import User


@login_required
def admin_panel(request):

    if request.user.role != 'admin':
        return redirect('/dashboard/')

    users_count = User.objects.count()

    return render(request, 'accounts/admin_panel.html', {
        'users_count': users_count,
    })


@login_required
def users_list(request):

    if request.user.role != 'admin':
        return redirect('/dashboard/')

    users = User.objects.all().order_by('id')

    return render(request, 'accounts/users_list.html', {
        'users': users
    })


@login_required
def change_user_role(request, user_id):

    if request.user.role != 'admin':
        return redirect('/dashboard/')

    user = get_object_or_404(
        User,
        id=user_id
    )

    new_role = request.POST.get('role')

    if new_role in ['admin', 'company', 'sales']:
        user.role = new_role
        user.save()

    return redirect('/admin-users/')