from django.db import models

# Create your models here.

class NewsItem(models.Model):
    name = models.TextField(blank=True,null=True)
    short = models.TextField(blank=True,null=True)
    long = models.TextField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    keywords = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    class Meta:
        ordering = ['-date']
