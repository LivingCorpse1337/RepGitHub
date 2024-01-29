from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from news.tasks import added_new_post


@receiver(m2m_changed, sender=PostCategory)
def notification_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        added_new_post.delay(instance.pk)

