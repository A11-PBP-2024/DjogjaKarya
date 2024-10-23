from django.db import models

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateField()
    last_modified = models.DateTimeField(auto_now=True)
    image = models.URLField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=False)
