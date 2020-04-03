# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import TaskItem, UpperPayment, LowerPayment, Invoice, InvoiceBatch, UpperToTask, LowerToOrder


class TaskItemRelateSerializer(serializers.ModelSerializer):
    upper_to_task = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = TaskItem
        fields = ['serial_id', 'upper_to_task', 'create_time', 'goods_owner', 'goods_name', 'weight', 'cube', 'amount', 'task_state', 'hash_value', 'txid', 'router', 'txid', 'invoice_status']


class UpperPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpperPayment
        fields = ['serial_id', 'create_time', 'invoice_org', 'goods_owner', 'amount', 'quantity', 'channel', 'txid']


class LowerPaymentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = LowerPayment
        fields = ['serial_id', 'create_time', 'invoice_org', 'broker', 'amount', 'quantity', 'channel', 'txid']


class InvoiceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Invoice
        fields = ['serial_id', 'create_time', 'channel', 'seller', 'buyer', 'amount', 'invoice_batch']


class InvoiceBatchSerializer(serializers.ModelSerializer):    
    invoice = serializers.StringRelatedField(many=True, read_only=True)
    taskitem = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = InvoiceBatch
        fields = ['batch_no', 'invoice', 'amount', 'taskitem']


class UpperToTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpperToTask
        fields = ['task', 'upper']
        

class LowerToOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = LowerToOrder
        fields = ['order', 'lower']