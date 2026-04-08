from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
import random
from .models import Post

@shared_task
def rotate_trending_post():
    posts = cache.get('posts')
    if not posts:
        posts = list(Post.objects.order_by('-created_at')[:20])
        if not posts:
            print("No posts found in database, skipping trending rotation")
            return 
    
    if hasattr(posts, '__iter__') and not isinstance(posts, list):
        posts = list(posts)
    
    trending_posts = random.sample(posts, min(len(posts), 3))

    channel_layer = get_channel_layer()
    for idx, post in enumerate(trending_posts, start=1):
        async_to_sync(channel_layer.group_send)('feed', {
            "type" : "new_post",
            "content" : post.content,
            "username" : post.display_name,
            "post_type" : "trending",
            "rank" : idx
        })