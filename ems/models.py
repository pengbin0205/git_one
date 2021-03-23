from django.db import models


# Create your models here.

class Department(models.Model):
    dept_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'dept'


class Employee(models.Model):
    name = models.CharField(max_length=20)
    age = models.SmallIntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    birthday = models.DateField(auto_now_add=True, null=True)
    gender = models.BooleanField()
    photo = models.ImageField(upload_to='img')
    dept = models.ForeignKey(to="Department", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'employee'
