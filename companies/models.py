from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=255)
    nip = models.CharField(max_length=20, unique=True)
    regon = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField()

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_company'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name