# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class TaskItemAdmin(admin.ModelAdmin):
    list_display = [
        'serial_id',
        'create_time',
        'goods_owner',
        'goods_name',
        'weight',
    ]

admin.site.register(TaskItem, TaskItemAdmin)


class UpperPaymentAdmin(admin.ModelAdmin):
    list_display = [
        'serial_id',
        'create_time',
        'invoice_org',
        'goods_owner',
        'amount',
    ]

admin.site.register(UpperPayment, UpperPaymentAdmin)


class LowerPaymentAdmin(admin.ModelAdmin):
    list_display = [
        'serial_id',
        'create_time',
        'invoice_org',
        'broker',
        'amount',
    ]

admin.site.register(LowerPayment, LowerPaymentAdmin)


class LowerToOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'lower',
        'created',
    ]

admin.site.register(LowerToOrder, LowerToOrderAdmin)


class UpperToTaskAdmin(admin.ModelAdmin):
    list_display = [
        'task',
        'upper',
        'created',
    ]

admin.site.register(UpperToTask, UpperToTaskAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'serial_id',
        'create_time',
        'channel',
        'seller',
        'buyer',
    ]

admin.site.register(Invoice, InvoiceAdmin)


class InvoiceBatchAdmin(admin.ModelAdmin):
    list_display = [
        'batch_no',
        'amount',
        'created',
    ]

admin.site.register(InvoiceBatch, InvoiceBatchAdmin)
