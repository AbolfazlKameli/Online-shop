# Generated by Django 5.0.6 on 2024-05-25 13:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, unique=True)),
                ('valid_from', models.DateTimeField()),
                ('expires_at', models.DateTimeField()),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(90, 'enter a value less than 90')])),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-paid', '-updated')},
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
