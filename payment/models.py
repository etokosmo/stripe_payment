from pathlib import Path

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


def get_upload_path(instance, filename):
    return Path(instance.name) / filename


class Item(models.Model):
    name = models.CharField(
        verbose_name="Имя",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True
    )
    price = models.DecimalField(
        verbose_name="Стоимость",
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to=get_upload_path,
        blank=True
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_firstname = models.CharField(
        verbose_name="Имя",
        max_length=50,
        default="No_name"  # TODO Add logic later
    )
    customer_lastname = models.CharField(
        verbose_name="Фамилия",
        max_length=50,
        default="No_lastname"  # TODO Add logic later
    )
    customer_address = models.CharField(
        verbose_name="Адрес",
        max_length=100,
        db_index=True,
        default="No_address"  # TODO Add logic later
    )
    registrated_at = models.DateTimeField(
        verbose_name="Время регистрации заказа",
        default=timezone.now,
        db_index=True
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'{self.customer_firstname} - {self.registrated_at}'


class OrderElements(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
        related_name='elements',
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        related_name='order_elements',
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество товара",
        validators=[MinValueValidator(1)]
    )
    price_in_order = models.DecimalField(
        verbose_name="Стоимость в заказе",
        max_digits=10,
        decimal_places=1,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f"{self.item} {self.order}"

    def get_item_price(self):
        return self.item.price
