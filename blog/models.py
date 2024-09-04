from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title

    def get_like_count(self):
        return self.postinteraction_set.filter(interaction_type='like').count()

    def get_dislike_count(self):
        return self.postinteraction_set.filter(interaction_type='dislike').count()
    
    def get_comment_count(self):
        return self.comments.count()

class PostInteraction(models.Model):
    INTERACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('post', 'user')


# ------------------------comment--------------

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user.username}: {self.content}'
    

    
    
    