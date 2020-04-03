# -*- coding: utf-8 -*-

from django.db import models
import django.db.models.deletion
from contract.models import OrderStart


class UpperPayment(models.Model):
    serial_id = models.CharField(max_length = 100,primary_key=True)
    create_time = models.DateTimeField(blank=True, null=True)
    invoice_org = models.CharField(max_length = 100)
    goods_owner = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    quantity = models.IntegerField(default=1)
    channel = models.CharField(max_length = 30)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)
    hash_value = models.BooleanField(default=False)
    txid = models.CharField(max_length = 100, blank=True, null=True)

    class Meta:
        ordering = ('-created',)


class LowerPayment(models.Model):
    serial_id = models.CharField(max_length = 100,primary_key=True)
    create_time = models.DateTimeField(blank=True, null=True)
    invoice_org = models.CharField(max_length = 100)
    broker = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    quantity = models.IntegerField(default=1)
    channel = models.CharField(max_length = 30)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)
    hash_value = models.BooleanField(default=False)
    txid = models.CharField(max_length = 100, blank=True, null=True)

    class Meta:
        ordering = ('-created',)


class LowerToOrder(models.Model):
    order = models.ForeignKey(OrderStart, related_name='lower_to_order',on_delete=django.db.models.deletion.CASCADE, blank=True, null=True)
    lower = models.ForeignKey(LowerPayment, related_name='lower_to_order',on_delete=django.db.models.deletion.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.lower.serial_id


class InvoiceBatch(models.Model):
    batch_no = models.CharField(max_length = 100,primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)


class Invoice(models.Model):
    serial_id = models.CharField(max_length = 100,primary_key=True)
    create_time = models.DateTimeField(blank=True, null=True)
    channel = models.CharField(max_length = 30)
    seller = models.CharField(max_length = 30)
    buyer = models.CharField(max_length = 30)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    invoice_batch = models.ForeignKey(InvoiceBatch,related_name='invoice',on_delete=django.db.models.deletion.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s : %f" % (self.serial_id, float(self.amount))


class TaskItem(models.Model):
    serial_id = models.CharField(max_length = 100,primary_key=True)
    create_time = models.DateTimeField(blank=True, null=True)
    goods_owner = models.CharField(max_length = 100)
    goods_name = models.CharField(max_length = 100)
    weight = models.DecimalField(max_digits=7, decimal_places=2,null=True)
    cube = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    invoice_batch = models.ForeignKey(InvoiceBatch,related_name='taskitem',on_delete=django.db.models.deletion.CASCADE, blank=True, null=True)
    task_state = models.BooleanField(default=True)
    invoice_status=models.BooleanField(default=False)
    router = models.CharField(max_length = 30)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)
    hash_value = models.BooleanField(default=False)
    txid = models.CharField(max_length = 100, blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "%s : %f" % (self.serial_id, float(self.amount))


class UpperToTask(models.Model):
    task = models.ForeignKey(TaskItem,related_name='upper_to_task',on_delete=django.db.models.deletion.CASCADE, blank=True, null=True)
    upper = models.ForeignKey(UpperPayment,related_name='upper_to_task',on_delete=django.db.models.deletion.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.upper.serial_id