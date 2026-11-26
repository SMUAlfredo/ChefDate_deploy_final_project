from django.db import models


class Cuisine(models.Model):
    name = models.CharField('display name', max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Chef(models.Model):
    name = models.CharField('display name', max_length=100)
    slug = models.SlugField(unique=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.PROTECT)
    base_price_cad = models.DecimalField(
        'base price per booking (CAD)',
        max_digits=10,
        decimal_places=2,
    )
    rating = models.DecimalField('demo rating', max_digits=2, decimal_places=1)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(base_price_cad__gte=0),
                name='catalog_chef_base_price_nonnegative',
            ),
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name='catalog_chef_rating_1_to_5',
            ),
        ]

    def __str__(self):
        return self.name
