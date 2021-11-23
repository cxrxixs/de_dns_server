from django.db import models


# Create your models here.
class DeDnsServerRaw(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(null=False)
    name = models.CharField(max_length=100, null=True)
    as_number = models.IntegerField(null=False)
    as_org = models.CharField(max_length=256, null=False)
    country_code = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=100, null=True)
    version = models.CharField(max_length=512, null=True)
    error = models.BooleanField(default=False, null=True)
    dnssec = models.BooleanField(null=True)
    reliability = models.DecimalField(max_digits=3, decimal_places=2)
    checked_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'de_dns_servers_raw'


class DeDnsServer(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(null=False)
    name = models.CharField(max_length=100, null=True)
    as_number = models.IntegerField(null=False)
    as_org = models.CharField(max_length=256, null=False)
    country_code = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=100, null=True)
    version = models.CharField(max_length=512, null=True)
    error = models.BooleanField(default=False, null=True)
    dnssec = models.BooleanField(null=True)
    reliability = models.DecimalField(max_digits=3, decimal_places=2)
    checked_at = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'de_dns_servers'


class ApiToken(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=6, unique=True)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True)

    class Meta:
        managed = True
        db_table = 'api_tokens'
