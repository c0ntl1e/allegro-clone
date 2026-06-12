from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.models import User
from .models import Message


@login_required
def inbox(request):

    users = User.objects.exclude(
        id=request.user.id
    )

    return render(
        request,
        'messages/inbox.html',
        {
            'users': users
        }
    )


@login_required
def conversation(request, user_id):

    other_user = get_object_or_404(
        User,
        id=user_id
    )

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('created_at')

    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    return render(
        request,
        'messages/conversation.html',
        {
            'messages': messages,
            'other_user': other_user
        }
    )


@login_required
def send_message(request, user_id):

    other_user = get_object_or_404(
        User,
        id=user_id
    )

    if request.method == 'POST':

        content = request.POST.get(
            'content'
        )

        if content:

            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )

    return redirect(
        f'/messages/{user_id}/'
    )