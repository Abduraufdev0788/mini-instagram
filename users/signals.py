from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Users, Profile


@receiver(post_save, sender=Users)
def create_default_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()