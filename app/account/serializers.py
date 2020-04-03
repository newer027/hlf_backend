# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import UserSettings
from contract.models import Vendor

class UserSettingsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserSettings
        fields = ['user', 'usernamename', 'realname', 'passwordword', 'created', 'telphone_num', 'comment', 'id']


class UserVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ['vendor']
        depth = 1


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'vendor']