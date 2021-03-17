# Generated by Django 3.1.7 on 2021-03-17 22:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survivor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survivor',
            name='age',
            field=models.DecimalField(decimal_places=0, default=None, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.RegexValidator('^[a-zA-Z ]{2,70}$', 'Name must be 2 to 70 characters long and alphabetical')]),
        ),
        migrations.AlterField(
            model_name='survivor',
            name='gender',
            field=models.CharField(default=None, max_length=1, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.RegexValidator('[MFO]', 'M, F or O')]),
        ),
        migrations.AlterField(
            model_name='survivor',
            name='items',
            field=models.CharField(default=None, max_length=120, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.RegexValidator('^Fiji Water:[0-9]*;Campbell Soup:[0-9]*;First Aid Pouch:[0-9]*;AK47:[0-9]*$', "Correct stock declaration format: 'Fiji Water:x;Campbell Soup:x;First Aid Pouch:x;AK47:x'(include all fields even if you have 0)")]),
        ),
    ]