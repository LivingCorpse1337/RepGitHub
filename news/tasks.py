from celery import shared_task
import datetime
from celery import shared_task
from news.models import Post, Category, PostCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from news.models import User, Author

@shared_task
def added_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    head = post.head
    preview = post.preview()
    subscribers_email = []

    for ctg in categories:
        subscribers = ctg.subscribers.all()
        subscribers_email += [s.email for s in subscribers]

        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': preview,
                'link': f'{settings.SITE_URL}/news/{pk}'
            }
        )

        msg = EmailMultiAlternatives(
            subject=head,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers,
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

@shared_task
def notification_every_week():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(creation_date__gt=last_week)
    categories = set(posts.values_list('categories__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))

    for user_id in subscribers:
        if user_id:
            user = User.objects.ger(id=user.id)
            user_is_author = Author.objects.filter(user_id=user_id).exists()
            if user_is_author:
                posts = posts.exclude(author=user.author)
            if posts:
                html_content = render_to_string(
                    'daily_post.html',
                    {
                    'link': settings.SITE_URL,
                    'posts': posts,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject='Новое за неделю',
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=subscribers,
                )

                msg.attach_alternative(html_content, 'text/html')
                msg.send()