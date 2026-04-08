from django.db import models
import string
import random

class Link(models.Model):
    original_url = models.URLField(verbose_name="Original URL")
    short_code = models.CharField(max_length=10, unique=True, verbose_name="Short Code")
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    @staticmethod
    def generate_code():
        length = 6
        characters = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(characters, k=length))
            if not Link.objects.filter(short_code=code).exists():
                return code
