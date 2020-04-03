# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include, path
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework import routers
from contract import views
from account import views as AccountViews
from payment import views as PaymentViews
from rest_framework_simplejwt import views as jwt_views
from django.views.generic import TemplateView

router = routers.DefaultRouter()

router.register(r'ledger', views.LedgerViewSet)
router.register(r'order', views.OrderItemViewSet)
router.register(r'orderstart', views.OrderStartViewSet)
router.register(r'account', AccountViews.UserSettingsViewSet)
router.register(r'createDistance', views.StatusDistanceViewSet)

router.register(r'taskitem', PaymentViews.TaskItemViewSet)
router.register(r'upperpayment', PaymentViews.UpperPaymentViewSet)
router.register(r'lowerpayment', PaymentViews.LowerPaymentViewSet)
router.register(r'invoice', PaymentViews.InvoiceViewSet)
router.register(r'invoicebatch', PaymentViews.InvoiceBatchViewSet)
router.register(r'lowertoorder', PaymentViews.LowerToOrderViewSet)
router.register(r'uppertotask', PaymentViews.UpperToTaskViewSet)

urlpatterns = [
    # url(r'^upload/', include(('upload.urls','upload'), namespace='upload')),
    # path(r'^api/v1/', include(router.urls)),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path("vendor_list/", AccountViews.VendorList.as_view(), name="vendor_list"),
    path("lastest_distance/", views.LastestStatusDistance.as_view(), name="lastest_distance"),
    path("lastest_abnormal/", views.LastestAbnormal.as_view(), name="lastest_abnormal"),
    path("order_end/", views.OrderEndView.as_view(), name="order_end"),
    path("order_detail/<slug:item_id>/", views.OrderDetail.as_view(), name="order_detail"),
    path("order_start/<slug:item_id>/", views.OrderStartDetail.as_view(), name="order_start"),
    path("order_end/<slug:item_id>/", views.OrderEndDetail.as_view(), name="order_end"),
    path("normal_item/", views.NormalItem.as_view(), name="normal_item"),
    path('users/current/', views.book_menu),
    path('dashboard/<int:start_y>/<int:start_m>/<int:start_d>/<int:end_y>/<int:end_m>/<int:end_d>/', views.dashboard),
    path('users/user_tree/', views.user_tree),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
]

urlpatterns += router.urls

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
