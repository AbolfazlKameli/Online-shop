# Generated by Django 5.0.6 on 2024-05-30 13:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_payinfo_options_alter_payinfo_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payinfo',
            name='id',
        ),
        migrations.AlterField(
            model_name='payinfo',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='orders.order'),
        ),
    ]