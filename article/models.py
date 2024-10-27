from django.db import models
from django.utils import timezone
import pytz


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    description = models.TextField()
    # Store only the date
    # You can set a specific timezone if needed
    publication_date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Convert publication_date to UTC+7 before saving
        local_tz = pytz.timezone('Asia/Jakarta')  # UTC+7 timezone
        # Set the date to today in the local timezone
        self.publication_date = timezone.now().astimezone(local_tz).date()
        super().save(*args, **kwargs)
