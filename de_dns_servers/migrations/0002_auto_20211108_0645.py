# Generated by Django 3.2.9 on 2021-11-08 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('de_dns_servers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dednsserver',
            name='ip_address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='dednsserverraw',
            name='ip_address',
            field=models.CharField(max_length=100),
        ),
    ]
