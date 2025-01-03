from django.db import models

# Create your models here.
# class Director(models.Model): 
#     # 导演（ID，姓名）
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=32, verbose_name='姓名', unique=True)

# class Actor(models.Model):
#     # 主演（ID，姓名）
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=32, verbose_name='姓名', unique=True)

class User(models.Model):
    # 用户（ID,用户名，密码，性别,年龄）
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.PositiveSmallIntegerField(verbose_name='年龄', null=True, blank=True)
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    # sex = models.CharField(max_length=1, verbose_name='性别', null=True, blank=True)
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices, null=True, blank=True)

class Film(models.Model):
    # 电影（ID,片名，年代，类型，拍摄国家,封面链接,评分,评论,主演列表，导演列表）
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='片名')
    year = models.PositiveSmallIntegerField(verbose_name='年代', null=True, blank=True)
    types = models.CharField(max_length=32, verbose_name='类型', null=True, blank=True)
    nationality = models.CharField(max_length=16, verbose_name='拍摄国家', null=True, blank=True)
    cover = models.CharField(max_length=128, verbose_name='封面链接', null=True, blank=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='评分', null=True, blank=True, default=0) # DecimalField
    comment = models.CharField(max_length=256, verbose_name='评论', null=True, blank=True, default="暂无评论")
    directors = models.CharField(max_length=64, verbose_name='导演列表', null=True, blank=True, default="暂无")
    actors = models.CharField(max_length=64, verbose_name='主演列表', null=True, blank=True, default="暂无")

class LoveDir(models.Model):
    # 收藏夹（ID,用户ID,名字,包含电影个数） cnt可能为不准确的数据，删除或增加Include是未更改（sql触发器把所有计数全加到最后一行），只在展示给用户时更新
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建者')
    name = models.CharField(max_length=32, verbose_name='收藏夹名')
    cnt = models.PositiveSmallIntegerField(verbose_name='包含电影个数', null=True, blank=True, default=0)

    def __str__(self):
        return self.name

# class Direct(models.Model):
#     # 执导（导演ID,电影ID）
#     director = models.ForeignKey(Director, on_delete=models.CASCADE, verbose_name='导演')
#     # to="Director", to_field="id", on_delete=models.SET_NULL, null=True, blank=True
#     film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name='电影')
#     class Meta:
#         unique_together = ("director", "film")

# class Act(models.Model):
#     # 出演（主演ID,电影ID）
#     actor = models.ForeignKey(Actor, on_delete=models.CASCADE, verbose_name='主演')
#     film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name='电影')
#     class Meta:
#         unique_together = ("actor", "film")

class Include(models.Model):
    # 包含（电影ID,收藏夹ID,时间）
    dir = models.ForeignKey(LoveDir, on_delete=models.CASCADE, verbose_name='收藏夹')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name='电影')
    date = models.DateField(verbose_name="收藏时间", auto_now=True)
    class Meta:
        unique_together = ("dir", "film")

# class Comment(models.Model):
#     # 评价（用户ID,电影ID,评分,评论）
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者')
#     film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name='电影')
#     score = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='评分') # DecimalField
#     comment = models.CharField(max_length=256, verbose_name='评论')
#     class Meta:
#         unique_together = ("user", "film")
