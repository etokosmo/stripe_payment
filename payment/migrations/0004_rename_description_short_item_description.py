# Generated by Django 4.1.2 on 2022-11-27 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_item_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='description_short',
            new_name='description',
        ),
    ]
