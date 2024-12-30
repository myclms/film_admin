# Generated by Django 5.1.3 on 2024-12-30 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('sex', models.CharField(max_length=1, verbose_name='性别')),
                ('nationality', models.CharField(max_length=15, verbose_name='国籍')),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('sex', models.CharField(max_length=1, verbose_name='性别')),
                ('nationality', models.CharField(max_length=15, verbose_name='国籍')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('age', models.SmallIntegerField(verbose_name='年龄')),
                ('sex', models.CharField(max_length=1, verbose_name='性别')),
                ('nationality', models.CharField(max_length=15, verbose_name='国籍')),
            ],
        ),
    ]
