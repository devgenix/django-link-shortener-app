from django.db import models
import string
import random

class Link(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_code():
        length = 6
        while True:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            if not Link.objects.filter(short_code=code).exists():
                return code
