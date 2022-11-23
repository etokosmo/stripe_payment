from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    name = models.CharField(
        verbose_name="Имя",
        max_length=200,
    )
    description_short = models.TextField(
        verbose_name="Описание",
        blank=True
    )
    price = models.DecimalField(
        verbose_name="Стоимость",
        max_digits=10,
        decimal_places=1,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
