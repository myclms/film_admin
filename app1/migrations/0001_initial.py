# Generated by Django 5.1.3 on 2024-12-30 12:33

import django.db.models.deletion
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
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='片名')),
                ('year', models.SmallIntegerField(null=True, verbose_name='年代')),
                ('types', models.CharField(max_length=32, null=True, verbose_name='类型')),
                ('nationality', models.CharField(max_length=16, null=True, verbose_name='拍摄国家')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('age', models.SmallIntegerField(null=True, verbose_name='年龄')),
                ('sex', models.CharField(max_length=1, null=True, verbose_name='性别')),
            ],
        ),
        migrations.CreateModel(
            name='LoveDir',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='收藏夹名')),
                ('count', models.IntegerField(verbose_name='包含电影个数')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.user', verbose_name='创建者')),
            ],
        ),
        migrations.CreateModel(
            name='Direct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.director', verbose_name='导演')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.film', verbose_name='电影')),
            ],
            options={
                'unique_together': {('director', 'film')},
            },
        ),
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.actor', verbose_name='主演')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.film', verbose_name='电影')),
            ],
            options={
                'unique_together': {('actor', 'film')},
            },
        ),
        migrations.CreateModel(
            name='Include',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='收藏时间')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.film', verbose_name='电影')),
                ('dir', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.lovedir', verbose_name='收藏夹')),
            ],
            options={
                'unique_together': {('dir', 'film')},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='评分')),
                ('comment', models.CharField(max_length=256, verbose_name='评论')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.film', verbose_name='电影')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.user', verbose_name='评论者')),
            ],
            options={
                'unique_together': {('user', 'film')},
            },
        ),
    ]
