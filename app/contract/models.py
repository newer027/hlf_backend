# -*- coding: utf-8 -*-

from django.db import models
import django.db.models.deletion


class Ledger(models.Model):
    serial_id = models.CharField(max_length = 100,primary_key=True)
    vendor = models.CharField(max_length = 100)
    invoice_org = models.CharField(max_length = 100)
    create_time = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)
    hash_value = models.BooleanField(default=False)
    txid = models.CharField(max_length = 100, blank=True, null=True)

    class Meta:
        ordering = ('-created',)


class OrderItem(models.Model):
    item_id = models.CharField(max_length = 100)
    serial_id = models.CharField(max_length = 100,null=True)
    vendor = models.CharField(max_length = 100)
    invoice_org = models.CharField(max_length = 100)
    create_time = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length = 100)
    start_short = models.CharField(max_length = 20)
    end_short = models.CharField(max_length = 20)
    palate = models.CharField(max_length = 100,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    ledger = models.ForeignKey(Ledger,related_name='order_to_ledger',on_delete=django.db.models.deletion.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)
    hash_value = models.BooleanField(default=False)
    txid = models.CharField(max_length = 100, blank=True, null=True)

    class Meta:
        ordering = ('-created',)


class OrderStart(models.Model):
    serial_id = models.CharField(max_length = 100)
    item_id = models.CharField(max_length = 100)
    create_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    start_loc = models.CharField(max_length = 100)
    start_short = models.CharField(max_length = 20)
    end_short = models.CharField(max_length = 20)
    vendor = models.CharField(max_length = 100)
    invoice_org = models.CharField(max_length = 100)
    palate = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    gps_time = models.DateTimeField(blank=True, null=True)
    gps_loc = models.CharField(max_length = 100)
    start_longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    start_latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    loc_source = models.CharField(max_length = 100)
    STATUS_CHOICE = ((0, 'No_Status'),(1, 'Normal'),(2, 'Start_Ng'),(3, 'End_Ng'),(4, 'StartEnd_Ng'))
    status=models.IntegerField(choices=STATUS_CHOICE, default=0)
    invoice_status=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)
    hash_value = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)
    txid = models.CharField(max_length = 100, blank=True, null=True)

    class Meta:
        ordering = ('-created',)

class OrderEnd(models.Model):
    serial_id = models.CharField(max_length = 100)
    end_time = models.DateTimeField(blank=True, null=True)
    end_loc = models.CharField(max_length = 100)
    gps_time = models.DateTimeField(blank=True, null=True)
    gps_loc = models.CharField(max_length = 100)
    end_longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    end_latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    loc_source = models.CharField(max_length = 100)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    updated = models.DateTimeField(auto_now=True)
    err_status = models.BooleanField(default=False)
    hash_value = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)
    txid = models.CharField(max_length = 100, blank=True, null=True)

    class Meta:
        ordering = ('-created',)


class Hashcode(models.Model):
    serial_id = models.CharField(max_length = 100)
    order_info = models.CharField(max_length = 800)
    order_hash = models.CharField(max_length = 100)
    txid = models.CharField(max_length = 100,primary_key=True)


class StatusDistance(models.Model):
    hours = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    velocity = models.DecimalField(max_digits=5, decimal_places=2, default=70.00)
    distance = models.DecimalField(max_digits=5, decimal_places=2, default=70.00)
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)


class Vendor(models.Model):
    vendor = models.CharField(max_length = 100)


class Abnormal(models.Model):
    orderStart = models.ForeignKey(OrderStart,related_name='abnormal',on_delete=django.db.models.deletion.CASCADE)
    serial_id = models.CharField(max_length = 100)
    item_id = models.CharField(max_length = 100)
    ngText = models.CharField(max_length = 100)
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)