# Generated by Django 3.1.4 on 2020-12-26 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_subscriptions_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='plan',
            field=models.IntegerField(default=0, null=True),
        ),
    ]