from django.db import models

# Create your models here.
class Director(models.Model): 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='姓名')
    sex = models.CharField(max_length=1, verbose_name='性别')
    nationality = models.CharField(max_length=15, verbose_name='国籍')

class Actor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='姓名')
    sex = models.CharField(max_length=1, verbose_name='性别')
    nationality = models.CharField(max_length=15, verbose_name='国籍')

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.SmallIntegerField(verbose_name='年龄')
    sex = models.CharField(max_length=1, verbose_name='性别')
    nationality = models.CharField(max_length=15, verbose_name='国籍')
