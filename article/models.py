from django.db import models

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateField()
    image = models.URLField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True)


class Comment(models.Model):
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name} - {self.content[:20]}"
