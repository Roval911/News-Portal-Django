from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings
from django.dispatch import receiver
from .models import PostCategory


def get_subscriber(category):
    email = []
    for user in category.subscribers.all():
        email.append(user.email)
    return email


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        template = 'account/email/new_post.html'

        for category in instance.category.all():
            email = f'Новый пост в категории:"{category}"'
            user = get_subscriber(category)
            html = render_to_string(
                template_name=template,
                context={
                    'category': category,
                    'post': instance,
                },
            )
            msg = EmailMultiAlternatives(
                subject=email,
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=user
            )

            msg.attach_alternative(html, 'text/html')
            msg.send()
