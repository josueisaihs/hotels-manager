from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Hotel, HotelChain, HotelDraft


@receiver(pre_save, sender=Hotel)
def hotel_signal_pre_save(instance: Hotel, **kargs) -> None:
    """
    Signal to assign the hotels to the instance
    """
    instance.assign_chain()


@receiver(post_save, sender=Hotel)
def hotel_signal_post_save(instance: Hotel, created: bool, **kargs) -> None:
    """
    Signal to assign the chain and related hotels to the instance
    If the instance is created, it sends an email to the recipient
    """

    instance.assign_related_hotels()

    if created:
        instance.creation_email_notification()


@receiver(pre_save, sender=HotelChain)
def hotel_chain_signal_pre_save(instance: HotelChain, **kwargs):
    instance.title = instance.title.title()


@receiver(post_save, sender=HotelDraft)
def hotel_draft_signal_post_save(instance: HotelDraft, created: bool, **kwargs):
    if created:
        instance.creation_email_notification()
