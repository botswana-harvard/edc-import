from django.db import models


class ShortenIdentifierName(models.Model):

    original_name = models.CharField(
        verbose_name='Original name.',
        max_length=50,
        unique=True)

    shorter_name = models.CharField(
        verbose_name='Shorter version of original name.',
        max_length=50)

    objects = models.Manager()

    class Meta:
        app_label = 'edc_import'
