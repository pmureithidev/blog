from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

# posts
class Post(models.Model):

    # draft/published 
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='blog_posts')
    body = models.TextField()

    # track the publish, created & update date and time
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
        )


    # let's add a unique way of ordering blogposts using the publish date
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', args=[self.publish.year,
                                            self.publish.month,
                                            self.publish.day,
                                            self.slug
                                            ])


# comments
class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
    
    def get_absolute_url(self):
        return reverse('post-detail', args=[self.publish.year,
                                            self.publish.month,
                                            self.publish.day,
                                            self.slug
                                            ])