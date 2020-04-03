# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from contract.models import OrderStart
from .models import TaskItem, UpperPayment, LowerPayment, Invoice, InvoiceBatch, LowerToOrder, UpperToTask
from .serializers import UpperPaymentSerializer, LowerPaymentSerializer, InvoiceSerializer, TaskItemRelateSerializer,\
    InvoiceBatchSerializer, UpperToTaskSerializer, LowerToOrderSerializer
from django.http import Http404
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import pytz
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum
from django.conf import settings
from django.db.models import F


class TaskItemFilter(filters.FilterSet):
    min_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='gte')
    max_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='lte')
    min_status = filters.BooleanFilter(field_name="task_state")
    
    class Meta:
        model = TaskItem
        fields = ['serial_id', 'min_create', 'max_create', 'min_status', 'goods_owner', 'invoice_status']


class TaskItemViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskItemRelateSerializer
    queryset = TaskItem.objects.all()
    filterset_class = TaskItemFilter


class UpperPaymentFilter(filters.FilterSet):
    min_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='gte')
    max_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='lte')
    
    class Meta:
        model = UpperPayment
        fields = ['min_create', 'max_create', 'serial_id', 'goods_owner', 'invoice_org']


class UpperPaymentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpperPaymentSerializer
    queryset = UpperPayment.objects.all()
    filterset_class = UpperPaymentFilter


class LowerPaymentFilter(filters.FilterSet):
    min_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='gte')
    max_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='lte')
    
    class Meta:
        model = LowerPayment
        fields = ['min_create', 'max_create', 'serial_id', 'broker', 'invoice_org']


class LowerPaymentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = LowerPaymentSerializer
    queryset = LowerPayment.objects.all()
    filterset_class = LowerPaymentFilter


class InvoiceFilter(filters.FilterSet):
    min_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='gte')
    max_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='lte')
    
    class Meta:
        model = Invoice
        fields = ['min_create', 'max_create', 'serial_id', 'seller', 'buyer']


class InvoiceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    filterset_class = InvoiceFilter


class InvoiceBatchViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = InvoiceBatchSerializer
    queryset = InvoiceBatch.objects.all()


class UpperToTaskViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpperToTaskSerializer
    queryset = UpperToTask.objects.all()

    def create(self, request):
        upper = request.data.get("upper")
        task = request.data.get("task")
        if UpperPayment.objects.filter(serial_id=upper):
            if TaskItem.objects.filter(serial_id=task):
                task_item = UpperPayment.objects.filter(serial_id=upper)[0]
                upper_item = TaskItem.objects.filter(serial_id=task)[0]
                task_item.invoice_status = True
                task_item.save()
                UpperToTask.objects.create(task=task, upper=upper)
                return Response({"task": task_item, "upper": upper_item}, status=status.HTTP_201_CREATED)
        return Response({"task": task, "upper": upper},
                            status=status.HTTP_400_BAD_REQUEST)



class LowerToOrderViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = LowerToOrderSerializer
    queryset = LowerToOrder.objects.all()

    def create(self, request):
        order = request.data.get("order")
        lower = request.data.get("lower")
        if OrderStart.objects.filter(serial_id=order):
            if LowerPayment.objects.filter(serial_id=lower):
                order_item = OrderStart.objects.filter(serial_id=order)[0]
                lower_item = LowerPayment.objects.filter(serial_id=lower)[0]
                order_item.invoice_status = True
                order_item.save()
                LowerToOrder.objects.create(order=order_item, lower=lower_item)
                return Response({"order": order, "lower": lower}, status=status.HTTP_201_CREATED)
        return Response({"order": order, "lower": lower},
                            status=status.HTTP_400_BAD_REQUEST)


"""
class OrderDetail(APIView):
    def get(self, request, item_id):
        if OrderStart.objects.filter(item_id=item_id):
            order_serial_id = OrderStart.objects.filter(item_id=item_id)[0].serial_id
            order_start = OrderStart.objects.filter(serial_id=order_serial_id)[0]
            start_serializer = OrderStartSerializer(order_start)
            newdict={}
            newdict.update(start_serializer.data)
            if OrderEnd.objects.filter(serial_id=order_start.serial_id, valid=True):
                order_end = OrderEnd.objects.filter(serial_id=order_start.serial_id, valid=True)[0]
                end_serializer = OrderEndSerializer(order_end)
                newdict.update(end_serializer.data)
                return Response(newdict, status=status.HTTP_201_CREATED)
            else:
                return Response(newdict, status=status.HTTP_201_CREATED)
        return Response("error", status=status.HTTP_400_BAD_REQUEST)


class MyView(APIView):
    queryset = TaskItem.objects.all().annotate(upper_to_task__upper=F('upper_to_task__upper'))
    serializer_class = OurModelSerializer
    pagination_class = settings.DEFAULT_PAGINATION_CLASS # cool trick right? :)

    # We need to override get method to achieve pagination
    def get(self, request):
        ...
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)


    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
         if self.paginator is None:
             return None
         return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
         assert self.paginator is not None
         return self.paginator.get_paginated_response(data)
"""