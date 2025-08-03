from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Message, MessageHistory



@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f"You have a new message from {instance.sender}"
        )
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id is not None:
        try:
            old_instance = Message.objects.get(id=instance.id)
            if old_instance.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_instance.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass
