from django.db import models


class Cuisine(models.Model):
    name = models.CharField('display name', max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
