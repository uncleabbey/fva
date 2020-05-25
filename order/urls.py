from django.urls import path, include
from .views import (
    OrderAPI,
    PreOrderAPI,
    OrderPayment,
    CancelOrderAPI,
    VendorUpdateOrderAPI,
    DailySalesAPI,
    NotificationAPI,
    OrderDetails
)

urlpatterns = [
    path('api/orders', OrderAPI.as_view(), name='order'),
    path('api/orders/<int:orderId>', OrderDetails.as_view(), name='Orderdetails'),
    path('api/orders/preorder', PreOrderAPI.as_view(), name='preorder'),
    path('api/orders/payment/<int:orderId>',
         OrderPayment.as_view(), name='payment'),
    path('api/orders/cancel/order/<int:orderId>',
         CancelOrderAPI.as_view(), name='cancel'),
    path('api/vendor/orders/change/status/<int:orderId>',
         VendorUpdateOrderAPI.as_view(), name='change-status'),
    path('api/orders/daily/sales', DailySalesAPI.as_view(), name='dailysales'),
    path('api/notifications', NotificationAPI.as_view(), name='notifications')
]
