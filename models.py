from django.db import models


# Create your models here.

class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")

    depart = models.ForeignKey(to="Department", to_field='id', on_delete=models.CASCADE)

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    """靓号管理"""
    mobile = models.CharField(verbose_name="号码", max_length=11, null=True, blank=True)  # ,
    """"
    !!!!!!  在 Python 中，只要你在变量后面加个逗号，它就会变成一个元组。

    你以为的：mobile 是一个 CharField 对象。
    
    实际情况：mobile 变成了一个 (CharField对象, ) 的元组。
    
    后果： Django 在读取你的模型时，发现 mobile、price 等是元组而不是 Field 对象，
    它就直接忽略了这些字段。所以，Django 确实去数据库创建了 app01_prettynum 表，
    但这个表里只有一个自动生成的 id 列，完全没有你定义的 mobile 和 price 等列。
    """

    price = models.IntegerField(verbose_name="价格", default=0)
    level_choice = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级'),
    )
    level = models.SmallIntegerField(verbose_name="等级", choices=level_choice, default=1)
    status_choice = (
        (1, '占用'),
        (2, '未占用'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice, default=2)
