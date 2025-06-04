from django.db import models
from django.utils import timezone
from datetime import timedelta
import string
import random

def default_expiry():
    return timezone.now() + timedelta(days=1)

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

class ShortURL(models.Model):
    orig_link = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)                         
    is_active = models.BooleanField(default=True)      
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry)

    class Meta:
        ordering = ['-created_at']

    def is_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
        super().save(*args, **kwargs)

class ClickStat(models.Model):
    short_url = models.ForeignKey(ShortURL, related_name='clicks', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)