# Generated by Django 5.0.6 on 2024-05-23 11:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('created',)},
        ),
        migrations.AddField(
            model_name='category',
            name='is_sub',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='s_category', to='home.category'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='product', to='home.category'),
        ),
    ]