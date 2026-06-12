from django.urls import path

from .views import (
    inbox,
    conversation,
    send_message
)

urlpatterns = [

    path(
        '',
        inbox,
        name='inbox'
    ),

    path(
        '<int:user_id>/',
        conversation,
        name='conversation'
    ),

    path(
        '<int:user_id>/send/',
        send_message,
        name='send_message'
    ),
]