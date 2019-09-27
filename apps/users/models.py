import traceback
from datetime import date

from django.db import models
from django.db import transaction
from django.db import IntegrityError, DataError
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as AuthUserManager

from utils.modelmanager import ModelManager

class UserManager(AuthUserManager, ModelManager):

    def add(self, account, password, **extra_fields):
        extra_fields.setdefault('account', account)
        return self.create_user(username=account, email=None, password=password, **extra_fields)


    def reset_password(self, account, password):
        """重置密码
        Arguments:
            cid {int} -- 用户id
        """
        user = self.filter(account=account).first()
        if user:
            user.set_password(password)
            user.save()



class User(AbstractUser):
    GENDER_UNSET = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICE = (
        (GENDER_UNSET, '未知'),
        (GENDER_MALE, '男'),
        (GENDER_FEMALE, '女'),
    )

    account = models.CharField(max_length=40, unique=True, verbose_name='账号')
    mini_openid = models.CharField(max_length=40, unique=True, null=True, blank=True, verbose_name='小程序账号')
    name = models.CharField(max_length=30, blank=True, verbose_name='昵称')
    age = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='年龄')
    gender = models.IntegerField(choices=GENDER_CHOICE, default=0, verbose_name='性别')
    avatar_url = models.CharField(max_length=300, blank=True, verbose_name='头像')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ['-id']
        verbose_name = verbose_name_plural = '用户信息'


mm_User = User.objects


class RelationShipManager(ModelManager):
    
    def add_relation(self, user, following):
        """添加关注
        """
        created, relation = self.get_or_create(user=user, following=following)
        return relation

    def remove_relation(self, user, following):
        """取消关注
        """
        self.filter(user=user, following=following).delete()

class RelationShip(models.Model):
    """用户关系"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following_set', verbose_name='我')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers_set', verbose_name='关注的人')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = RelationShipManager()

    class Meta:
        db_table = 'user_relationship'
        index_together = [
            ['user', 'following']
        ]
        unique_together = [
            ['user', 'following']
        ]


mm_RelationShip = RelationShip.objects


class PointManager(ModelManager):
    POINT_OUT = 0
    POINT_IN = 1
    POINT_OP_CHOICE = (
        (POINT_OUT, '减少'),
        (POINT_IN, '增加'),
    )

    ATION_CHECK_IN = 0

    ACTION_CHOICE = (
        (ATION_CHECK_IN, '每日签到'),
    )

    Action_Point_Mapping = {
        ATION_CHECK_IN: 30,
    }

    Action_Desc = {action: msg for action, msg in ACTION_CHOICE}

    def get_total_point(self, user_id):
        record = self.filter(user_id=user_id).first()
        if record:
            return record.total_left
        else:
            return 0

    def _add_action(self, user_id, action, amount, total_left, operator_id=None):
        """
        积分记录
        :param customer_id: 用户id
        :param amount: 操作总量
        :param action: 行为
        :param operator_id: 操作人auth_user.id
        :return:
        """
        in_or_out = self.POINT_IN
        self.create(user_id=user_id,
                    in_or_out=in_or_out,
                    amount=amount,
                    total_left=total_left,
                    action=action,
                    desc=self.Action_Desc[action],
                    operator_id=operator_id,
                    )

    def add_action(self, user_id, action):
        """
        增加积分记录
        :param customer_id:
        :param action:
        :return:
        """
        amount = self.Action_Point_Mapping[action]
        total_left = self.get_total_point(user_id) + amount
        self._add_action(user_id=user_id,
                         action=action,
                         amount=amount,
                         total_left=total_left,
                         )


class Point(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='points',
                             verbose_name='用户')
    in_or_out = models.PositiveSmallIntegerField(choices=PointManager.POINT_OP_CHOICE,
                                                 default=PointManager.POINT_IN,
                                                 verbose_name='增加|减少')
    amount = models.PositiveSmallIntegerField(default=0, verbose_name='数量')
    total_left = models.PositiveIntegerField(default=0, verbose_name='剩余数量')
    action = models.PositiveSmallIntegerField(
        choices=PointManager.ACTION_CHOICE, default=0, verbose_name='原因')
    desc = models.CharField(verbose_name='描述', max_length=48)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 null=True, blank=True, verbose_name='操作人')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    objects = PointManager()

    class Meta:
        db_table = 'user_points'
        ordering = ['-create_at']


mm_Point = Point.objects


class CheckInManager(ModelManager):
    
    def is_check_in(self, user_id):
        return self.filter(user_id=user_id, create_at__gt=date.today()).exists()

class CheckIn(models.Model):
    """用户签到表
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='用户')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    objects = CheckInManager()

    class Meta:
        db_table = 'user_checkin'


mm_CheckIn = CheckIn.objects

