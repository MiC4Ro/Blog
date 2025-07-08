from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
     # Методы для работы с комментариями
    def add_comment(self, author, text):
        return Comment.objects.create(post=self, author=author, text=text)

    def get_comments(self):
        return self.comments.filter(active=True)

    def get_comments_count(self):
        return self.comments.filter(active=True).count()
    
     #Методы для работы с лайками
    def add_like(self, user):
        like, created = Like.objects.get_or_create(post=self, user=user)
        if not created:
            like.delete()
            return False
        return True
    
    def get_likes_count(self):
        return self.likes.count()
    
    def is_liked_by_user(self, user):
        if user.is_anonymous:
            return False
        return self.likes.filter(user=user).exists()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True) #Для модерации комментариев

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'user')  # Один пользователь может лайкнуть пост только один раз

    def __str__(self):
        return f'{self.user} likes {self.post}'