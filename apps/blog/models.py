from uuid import uuid4

from django.db import models
from apps.user.models import User


class BlogCategory(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    category = models.CharField(max_length=64, null=False, unique=True)

    class Meta:
        ordering = ('category',)
        verbose_name = 'BlogCategory'
        verbose_name_plural = 'BlogCategories'

    def __str__(self):
        return f"BlogCategory(id={self.uuid}, category={self.category})"


class Blog(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=64, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    image = models.ImageField(blank=True)
    text = models.TextField(max_length=1024, blank=True)
    active = models.BooleanField(default=True)
    publish_data = models.DateField(auto_now=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return f"Blog(id={self.uuid}, title={self.title}, category={self.category})"


