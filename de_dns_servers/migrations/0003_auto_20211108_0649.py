# Generated by Django 3.2.9 on 2021-11-08 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('de_dns_servers', '0002_auto_20211108_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dednsserver',
            name='ip_address',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='dednsserverraw',
            name='ip_address',
            field=models.GenericIPAddressField(),
        ),
    ]