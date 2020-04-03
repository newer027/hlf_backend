# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from .models import UserSettings
from contract.models import Vendor
from rest_framework import status
from .serializers import UserSettingsSerializer, UserVendorSerializer, VendorSerializer
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import decorators
from rest_framework import parsers
from rest_framework.views import APIView


class UserSettingsFilter(filters.FilterSet):
    min_create = filters.DateTimeFilter(field_name="created", lookup_expr='gte')
    max_create = filters.DateTimeFilter(field_name="created", lookup_expr='lte')
    
    class Meta:
        model = UserSettings
        fields = ['usernamename', 'realname', 'telphone_num', 'min_create', 'max_create']


class UserSettingsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSettingsSerializer
    queryset = UserSettings.objects.all()
    filterset_class = UserSettingsFilter

    def create(self, request):
        serializer = UserSettingsSerializer(data=request.data)
        if UserSettings.objects.filter(usernamename=request.data.get("usernamename")):
            return Response({"usernamename": request.data.get("usernamename")}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            username = request.data.get('usernamename').replace(' ', '')
            password = request.data.get('passwordword')
            user = User.objects.create(username=username)
            user.set_password(password)
            user.is_active = True
            user.save()
            if UserSettings.objects.filter(usernamename=request.data.get("usernamename")):
                UserSettings.objects.filter(usernamename=request.data.get("usernamename")).update(user=user)
                return Response({"usernamename": request.data.get("usernamename")}, status=status.HTTP_201_CREATED)
        return Response({"usernamename": request.data.get("usernamename")}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        UserSettings.objects.filter(pk=pk).update(realname = request.data.get("realname"), usernamename=request.data.get("usernamename"),
            passwordword = request.data.get("passwordword"), telphone_num = request.data.get("telphone_num"), comment = request.data.get("comment"))
        user = UserSettings.objects.filter(pk=pk)[0].user
        user.usernamename=request.data.get("usernamename")
        user.set_password(request.data.get("passwordword"))
        user.save()
        return Response({"usernamename": request.data.get("usernamename")}, status=status.HTTP_201_CREATED)
        
    def destroy(self, request, pk):
        user = UserSettings.objects.filter(pk=pk)[0].user
        user.delete()
        UserSettings.objects.filter(pk=pk).delete()
        return Response({"usernamename": "success"}, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk):
        if UserSettings.objects.filter(pk=pk):
            user_settings = UserSettings.objects.filter(pk=pk)[0]
            user_settings_serializer = UserVendorSerializer(user_settings)
            return Response(user_settings_serializer.data, status=status.HTTP_201_CREATED)
        return Response({"pk": pk}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(
        detail=True,
        methods=['PUT'],
        serializer_class=UserVendorSerializer,
    )
    def vendor_list(self, request, pk):
        obj = self.get_object()
        for existing_subject in obj.vendor.all():
            obj.vendor.remove(existing_subject)
        values = request.data.get('vendor')
        list = values.split (",")
        li = []
        for i in list:
            if len(i)>0:
                li.append(int(i))
        subjects = Vendor.objects.filter(pk__in = li)
        for subject in subjects:
            obj.vendor.add(subject)
        return Response("success", status=status.HTTP_201_CREATED)


class VendorList(APIView):
    def get(self, request, format=None):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
