# -*- coding: utf-8 -*-

# from openpyxl import load_workbook
# from openpyxl.compat import range
from celery import Celery
import time
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger
import hashlib 
from celery import Task
from hello_django.settings import BASE_DIR
import os, requests
from .models import Hashcode, OrderItem, Ledger, OrderStart, OrderEnd, StatusDistance, Abnormal
from django.contrib.contenttypes.models import ContentType
from celery.task.schedules import crontab
from django.core import serializers
from math import sin, asin, cos, radians, fabs, sqrt

EARTH_RADIUS=6371           # 地球平均半径，6371km
logger = get_task_logger(__name__)


class TaskError(Exception):
    """Custom exception for handling task errors"""
    pass


class ServiceError(Exception):
    """Custom exception for service errors"""
    pass


class AppBaseTask(Task):
    """Base Task

    The base Task class can be used to define
    shared behaviour between tasks.

    """

    abstract = True

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # TODO: log out here
        super(AppBaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # TODO: log out here
        super(AppBaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)


@task(base=AppBaseTask, bind=True, max_retries=3, soft_time_limit=125)
def sha256_to_block(self, source, pk, which):
    sha256_hash = hashlib.sha256()
    hash_str = ""
    txid = ""
    try:
        sha256_hash.update(source.encode('utf-8'))
        hash_str = sha256_hash.hexdigest()
        r = requests.post('http://10.10.70.137:3030/api/v1/string/', json = {'shaResult': hash_str})
        if r.status_code == 500:
            raise ServiceError
        txid = r.text

    except ServiceError as se:
        self.retry(countdown=10, exc=se)
    except Exception as exc:
        raise TaskError(exc)
    if which == 1:
        OrderItem.objects.filter(pk=pk).update(txid=txid)
    elif which == 2:
        OrderStart.objects.filter(pk=pk).update(txid=txid)
    elif which == 3:
        OrderEnd.objects.filter(pk=pk).update(txid=txid)
    else:
        Ledger.objects.filter(pk=pk).update(txid=txid)
    create_hashcode(pk, source, hash_str, txid)
    return hash_str


def create_hashcode(serial_id, order_info, order_hash, txid):
    hashcode = Hashcode(serial_id=serial_id, order_info=order_info,
        order_hash=order_hash, txid=txid)
    hashcode.save()


@task(base=AppBaseTask, bind=True, max_retries=3, soft_time_limit=125)
def start_end_error(self, lat0, lng0, loc, pk, which):
    try:
        r = requests.get("http://api.map.baidu.com/geocoder?address="+ loc +"&output=json&key=yCM2VbguexR2Rccne1Tgamd2FwoRiXwV")
        r_json = r.json()
        lng1 = r_json["result"]["location"]["lng"]
        lat1 = r_json["result"]["location"]["lat"]
    except ServiceError as se:
        self.retry(countdown=10, exc=se)
    except Exception as exc:
        raise TaskError(exc)
    distance = get_distance_hav(lat0, lng0, lat1, lng1)
    distance_rule = StatusDistance.objects.first()
    distance_limit = distance_rule.hours * distance_rule.velocity
    status_flag = float(distance_limit) < distance
    if which == 1:
        if status_flag:
            OrderStart.objects.filter(pk=pk).update(status=2)
            Abnormal.objects.create(orderStart=OrderStart.objects.filter(pk=pk)[0], serial_id=OrderStart.objects.filter(pk=pk)[0].serial_id, item_id=OrderStart.objects.filter(pk=pk)[0].item_id, ngText="出发地异常")
        else:
            OrderStart.objects.filter(pk=pk).update(status=1)
    else:
        serial_id = OrderEnd.objects.get(pk=pk).serial_id
        if OrderStart.objects.filter(serial_id=serial_id)[0].status == 0:
            pass
        if OrderStart.objects.filter(serial_id=serial_id)[0].status == 1:
            if status_flag:
                OrderStart.objects.filter(serial_id=serial_id).update(status=3)
                Abnormal.objects.create(orderStart=OrderStart.objects.filter(pk=pk)[0], serial_id=OrderStart.objects.filter(pk=pk)[0].serial_id, item_id=OrderStart.objects.filter(pk=pk)[0].item_id, ngText="到达地异常")
        else:
            if status_flag:
                OrderStart.objects.filter(serial_id=serial_id).update(status=4)
                Abnormal.objects.create(orderStart=OrderStart.objects.filter(pk=pk)[0], serial_id=OrderStart.objects.filter(pk=pk)[0].serial_id, item_id=OrderStart.objects.filter(pk=pk)[0].item_id, ngText="出发地到达地异常")
        OrderEnd.objects.filter(pk=pk).update(err_status=True)


@periodic_task(
    run_every=(crontab(minute='*/3')),
    name="asins_depart",
    ignore_result=True
)
def asins_depart():
    logger.info("Saved latest asins_depart")
    start = time.time()
    for order3 in OrderStart.objects.filter(status=0):
        if (time.time()-start)<60:
            start_end_error.delay(float(order3.start_latitude), float(order3.start_longitude), order3.start_loc, order3.pk, 1)
    for order4 in OrderEnd.objects.filter(err_status=False):
        if (time.time()-start)<60:
            start_end_error.delay(float(order4.end_latitude), float(order4.end_longitude), order4.end_loc, order4.pk, 2)
    for order0 in OrderItem.objects.filter(hash_value=False):
        if (time.time()-start)<60:
            OrderItem.objects.filter(serial_id=order0.serial_id).update(hash_value=True)
            sha256_to_block.delay(str(serializers.serialize('json', [ order0, ])),order0.pk, 1)
            time.sleep(0.12)
    for order1 in OrderStart.objects.filter(hash_value=False):
        if (time.time()-start)<60:
            OrderStart.objects.filter(serial_id=order1.serial_id).update(hash_value=True)
            sha256_to_block.delay(str(serializers.serialize('json', [ order1, ])),order1.pk, 2)
            time.sleep(0.12)
    for order2 in OrderEnd.objects.filter(hash_value=False):
        if (time.time()-start)<60:
            OrderEnd.objects.filter(serial_id=order2.serial_id).update(hash_value=True)
            sha256_to_block.delay(str(serializers.serialize('json', [ order2, ])),order2.pk, 3)
            time.sleep(0.12)
    for ledger in Ledger.objects.filter(hash_value=False):
        if (time.time()-start)<60:
            Ledger.objects.filter(serial_id=ledger.serial_id).update(hash_value=True)
            sha256_to_block.delay(str(serializers.serialize('json', [ ledger, ])),ledger.pk, 4)
            time.sleep(0.12)


def hav(theta):
    s = sin(theta / 2)
    return s * s
 


def get_distance_hav(lat0, lng0, lat1, lng1):
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
 
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    return distance
    