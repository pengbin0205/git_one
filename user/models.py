from django.db import models


# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    sex = models.BooleanField(default=True, verbose_name="True为男")
    phone = models.CharField(max_length=11)
    salt = models.CharField(max_length=8, default=None, null=True)

    class Meta:
        db_table = 'user'
