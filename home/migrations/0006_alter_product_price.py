# Generated by Django 5.0.6 on 2024-05-26 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]