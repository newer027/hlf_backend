# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Ledger, OrderItem, OrderStart, OrderEnd, StatusDistance, Abnormal


class LedgerSerializer(serializers.Serializer):
    serial_id = serializers.CharField()
    vendor = serializers.CharField()
    invoice_org = serializers.CharField()
    create_time = serializers.DateTimeField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        return Ledger.objects.create(**validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    lower_to_order = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['item_id', 'serial_id', 'vendor', 'invoice_org', 'create_time', 'category', 'end_short', 'start_short', 'palate', 'amount', 'ledger', 'txid', 'hash_value', 'invoice_status', 'lower_to_order']


class OrderStartSerializer(serializers.ModelSerializer):
    lower_to_order = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = OrderStart
        fields = ['serial_id', 'item_id', 'create_time', 'start_time', 'start_loc', 'end_short', 'start_short', 'vendor', 'invoice_org', 'palate', 'amount', 'txid',
        'gps_time', 'gps_loc', 'start_longitude', 'start_latitude', 'status', 'loc_source', 'lower_to_order']


class OrderEndSerializer(serializers.ModelSerializer):    
    class Meta:
        model = OrderEnd
        fields = ['serial_id', 'end_time', 'end_loc', 'txid','gps_time', 'gps_loc', 'end_longitude', 'end_latitude', 'loc_source']


class StatusDistanceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = StatusDistance
        fields = ['hours', 'velocity', 'distance', 'created']


class AbnormalSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Abnormal
        fields = ['orderStart', 'ngText', 'serial_id', 'item_id', 'created']
