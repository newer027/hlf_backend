from django.db import models
from django.contrib.auth.models import User
import django.db.models.deletion
from contract.models import Vendor


class UserSettings(models.Model):
    """
    Model to store additional user settings and preferences. Extends User
    model.
    """
    user = models.OneToOneField(User,related_name='settings',on_delete=django.db.models.deletion.CASCADE, null=True)
    usernamename = models.CharField(max_length=20)
    realname = models.CharField(max_length=20)
    passwordword = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    telphone_num = models.CharField(max_length=20)
    comment = models.TextField(null=True)
    vendor = models.ManyToManyField(Vendor, related_name="user_settings")

    def username(self):
        return self.user.username
    username.admin_order_field = 'user__username'

    class Meta:
        verbose_name_plural = 'User Settings'