# Generated by Django 5.1.3 on 2025-01-05 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_usercnt'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserCnt',
        ),
        migrations.AlterField(
            model_name='film',
            name='actors',
            field=models.CharField(blank=True, default='暂无', max_length=256, null=True, verbose_name='主演列表'),
        ),
        migrations.AlterField(
            model_name='film',
            name='comment',
            field=models.CharField(blank=True, default='暂无评论', max_length=512, null=True, verbose_name='评论'),
        ),
    ]
