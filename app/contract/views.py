# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from .models import Ledger, OrderItem, OrderStart, OrderEnd, Vendor, StatusDistance, Abnormal
from .serializers import LedgerSerializer, OrderItemSerializer, OrderStartSerializer, OrderEndSerializer, StatusDistanceSerializer, AbnormalSerializer
from django.http import Http404
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from account.models import UserSettings
import pytz
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum
import jwt


class OrderStartFilter(filters.FilterSet):
    min_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='gte')
    max_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='lte')
    min_status = filters.NumberFilter(field_name="status", lookup_expr='gte')
    
    class Meta:
        model = OrderStart
        fields = ['item_id', 'vendor', 'invoice_org', 'min_create', 'max_create', 'status', 'palate', 'serial_id', 'min_status', 'invoice_status']


class OrderStartViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderStartSerializer
    queryset = OrderStart.objects.filter(valid=True)
    filterset_class = OrderStartFilter
    
    def get_queryset(self):
        vendor_qs = Vendor.objects.filter(user_settings__usernamename=str(self.request.user)).values('vendor')
        queryset = OrderStart.objects.filter(vendor__in=vendor_qs, valid=True)
        return queryset

    def create(self, request):
        if OrderStart.objects.filter(serial_id=request.data.get("serial_id")):
            OrderStart.objects.filter(serial_id=request.data.get("serial_id")).update(valid=False)
        if not Vendor.objects.filter(vendor=request.data.get("vendor")):
            Vendor.objects.create(vendor=request.data.get("vendor"))
        serializer = OrderStartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderEndView(APIView):

    def post(self, request, format=None):
        if OrderEnd.objects.filter(serial_id=request.data.get("serial_id")):
            OrderEnd.objects.filter(serial_id=request.data.get("serial_id")).update(valid=False)
        serializer = OrderEndSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderStartDetail(APIView):
    def get(self, request, item_id):
            serial_id = OrderStart.objects.filter(item_id=item_id)[0].serial_id
            order_start = OrderStart.objects.filter(serial_id=serial_id)
            start_serializer = OrderStartSerializer(order_start, many=True)
            return Response(start_serializer.data, status=status.HTTP_201_CREATED)


class OrderEndDetail(APIView):
    def get(self, request, item_id):
        order_start = OrderStart.objects.filter(item_id=item_id)[0]
        order_end = OrderEnd.objects.filter(serial_id=order_start.serial_id)
        end_serializer = OrderEndSerializer(order_end, many=True)
        return Response(end_serializer.data, status=status.HTTP_201_CREATED)


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


class NormalItem(APIView):
    def get_object(self, item_id):
        try:
            return OrderStart.objects.filter(item_id=item_id)[0]
        except OrderStart.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        item_id = request.data.get("item_id")
        order_start = self.get_object(item_id)
        ledger_id = request.data.get("ledger")
        if not Ledger.objects.filter(serial_id=ledger_id):
            ledger_serializer = LedgerSerializer(data={"serial_id": ledger_id, "vendor": request.data.get("vendor"),
                "invoice_org": request.data.get("invoice_org"), "create_time": request.data.get("create_time"), "amount": request.data.get("amount")})
            if ledger_serializer.is_valid():
                ledger_serializer.save()
        if Ledger.objects.filter(serial_id=ledger_id):
            ledger = Ledger.objects.filter(serial_id=ledger_id)[0]
            dict_item={"serial_id": order_start.serial_id, "item_id": order_start.item_id, 
                "vendor": order_start.vendor, "create_time": order_start.create_time, 
                "category": "normal", "start_short": order_start.start_short, "end_short": order_start.end_short, "invoice_org": order_start.invoice_org, 
                "palate": order_start.palate, "amount": order_start.amount, "ledger": ledger}
            order_item = OrderItem(**dict_item)
            order_item.save()
            return Response({"serial_id": order_start.serial_id}, status=status.HTTP_201_CREATED)
        return Response({"serial_id": order_start.serial_id}, status=status.HTTP_400_BAD_REQUEST)


class LedgerFilter(filters.FilterSet):
    min_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='gte')
    max_create = filters.DateTimeFilter(field_name="create_time", lookup_expr='lte')
    
    class Meta:
        model = Ledger
        fields = ['serial_id', 'vendor', 'invoice_org', 'min_create', 'max_create']


class LedgerViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = LedgerSerializer
    queryset = Ledger.objects.all()
    filterset_class = LedgerFilter


class OrderFilter(filters.FilterSet):
    class Meta:
        model = OrderItem
        fields = ['ledger']


class OrderItemViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    filterset_class = OrderFilter

    def create(self, request):
        ledger_id = request.data.get("ledger")
        if Ledger.objects.filter(serial_id=ledger_id):
            ledger = Ledger.objects.filter(serial_id=ledger_id)[0]
            dict_item={"item_id": request.data.get("item_id"), 
                "vendor": request.data.get("vendor"), "create_time": request.data.get("create_time"), 
                "category": "modified", "start_short": request.data.get("start_short"), "end_short": request.data.get("end_short"), "invoice_org": request.data.get("invoice_org"), 
                "amount": request.data.get("amount"), "ledger": ledger}
            order_item = OrderItem(**dict_item)
            order_item.save()
            return Response({"item_id": request.data.get("item_id")}, status=status.HTTP_201_CREATED)
        return Response({"item_id": request.data.get("item_id")},
                            status=status.HTTP_400_BAD_REQUEST)
                            

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['roles'] = ['ROLE_ADMIN']
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def book_menu(request):
    item_id = jwt.decode(request.META['HTTP_AUTHORIZATION'][7:], None, None)['user_id']
    user_id = User.objects.filter(id=item_id)[0].username
    if str(user_id) == 'ubuntu':
        userInfoMap = { 'msg': 'success', 'code': 0, 'data': { 'user': { 'userId': 1, 'username': user_id, 'password': '', 'openId': '', 'mobile': '', 'picUrl': 'static/img/user.png', 'statu': 0, 'createTime': '', 'updateTime': '', 'roleList': [] }, 'permissions': ['user_view', 'user_del', 'user_upd', 'user_add'], 'roles': ['ROLE_ADMIN'] }}
    else:
        userInfoMap = { 'msg': 'success', 'code': 0, 'data': { 'user': { 'userId': 1, 'username': user_id, 'password': '', 'openId': '', 'mobile': '', 'picUrl': 'static/img/user.png', 'statu': 0, 'createTime': '', 'updateTime': '', 'roleList': [] }, 'permissions': ['user_view', 'user_del', 'user_upd', 'user_add'], 'roles': ['ROLE'] }}
    return JsonResponse(userInfoMap, safe=False)


def user_tree(request):
    item_id = jwt.decode(request.META['HTTP_AUTHORIZATION'][7:], None, None)['user_id']
    user_id = User.objects.filter(id=item_id)[0].username
    if str(user_id) == 'ubuntu':
        userTree = [8, 7, 10, 9, 14, 1, 5, 3, 11, 4, 13, 6, 12]
    else:
        userTree = [2]
    return JsonResponse(userTree, safe=False)


class LastestStatusDistance(APIView):
    def get(self, request, format=None):
        statusDistance = StatusDistance.objects.first()
        serializer = StatusDistanceSerializer(statusDistance)
        return Response(serializer.data)


class StatusDistanceViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = StatusDistanceSerializer
    queryset = StatusDistance.objects.all()


class LastestAbnormal(APIView):
    def get(self, request, format=None):
        abnormals = Abnormal.objects.all()[:10]
        serializer = AbnormalSerializer(abnormals, many=True)
        return Response(serializer.data)


def dashboard(request, start_y, start_m, start_d, end_y, end_m, end_d):
    sh_tz = pytz.timezone("Asia/Shanghai")
    start_time =  sh_tz.localize(datetime(start_y, start_m, start_d, 0, 0, 0))
    end_time =  sh_tz.localize(datetime(end_y, end_m, end_d, 23, 59, 59))
    order_list = OrderStart.objects.filter(create_time__gte=start_time, create_time__lte=end_time, valid=True)
    # truck_quantity = order_list.distinct('palate').count() "truck_quantity": truck_quantity, 
    order_quantity = order_list.count()
    amount = order_list.aggregate(order_amount=Sum('amount'))
    if order_quantity == 0:
        abnormal_percent = 0
    else:
        abnormal_percent = order_list.filter(status__gt=1).count() * 100 / order_quantity
    if amount['order_amount']:
        order_amount = amount['order_amount']
    else:
        order_amount = 0
    return JsonResponse({"order_quantity": order_quantity, "amount": round(order_amount, 2), "abnormal_percent": abnormal_percent}, safe=False)