from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import *

@receiver(post_save, sender=Post)
def broadcast_new_post(sender, instance, created, **kwargs):
    if created:
        layer = get_channel_layer()
        async_to_sync(layer.group_send)('feed', {
            'type' : 'new_post',
            'content' : instance.content,
            'username' : instance.display_name
        })