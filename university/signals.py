from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import College
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=College)
def announce_new_college(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "colleges",
            {
                "type": "new_college",
                "message": f"New college added: {instance.name}"
            }
        )
