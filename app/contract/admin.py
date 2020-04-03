# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class LedgerAdmin(admin.ModelAdmin):
    list_display = [
        'serial_id',
        'vendor',
        'invoice_org',
        'create_time',
        'amount',
    ]

admin.site.register(Ledger, LedgerAdmin)


class OrderStartAdmin(admin.ModelAdmin):
    list_display = [
        'serial_id',
        'create_time',
        'amount',
    ]

admin.site.register(OrderStart, OrderStartAdmin)


class OrderEndAdmin(admin.ModelAdmin):
    list_display = [
        'serial_id',
    ]

admin.site.register(OrderEnd, OrderEndAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'serial_id',
        'create_time',
    ]

admin.site.register(OrderItem, OrderItemAdmin)


class HashcodeAdmin(admin.ModelAdmin):
    list_display = [
        'serial_id',
        'order_info',
        'order_hash',
        'txid',
    ]

admin.site.register(Hashcode, HashcodeAdmin)


class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'vendor',
    ]

admin.site.register(Vendor, VendorAdmin)


class StatusDistanceAdmin(admin.ModelAdmin):
    list_display = [
        'hours', 'velocity', 'distance', 'created'
    ]

admin.site.register(StatusDistance,StatusDistanceAdmin)

class AbnormalAdmin(admin.ModelAdmin):
    list_display = [
        'orderStart', 'serial_id', 'ngText', 'created'
    ]

admin.site.register(Abnormal, AbnormalAdmin)
