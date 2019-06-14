from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_published = models.DateTimeField(default=timezone.now)
    post_content = models.TextField()
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    post_image = models.ImageField(null=True, blank=True, height_field="height_field", width_field="width_field")
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
    	return self.post_title

    class Meta:
        ordering = ['-post_published']