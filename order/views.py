from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import (
    generics,
    mixins,
    permissions,
    status,
    views,
    viewsets
)

from rest_framework.response import Response
from django.db import models


from accounts.models import Customer, User, Vendor
from menu.models import Menu
from menu.serializers import MenuSerializers
from menu.permissions import IsVendorOrReadOnly
from .permissions import IsOwnerOrReadOnly
from .models import (
    Order,
    OrderStatus,
    PreOrder,
    ItemsOrdered,
    Notification,
    MessageStatus
)
from .serializers import (
    OrderSerializer,
    CustomerSerializer,
    PreorderSerializer,
    ItemOrderedSerializer,
    ItemListSerializer,
    NotificationSerializer,
    CreateOrderSerializer,
    CreatePreorderSerializer
)
from .helper import send_notification, get_status
# Create your views here.


class OrderAPI(generics.ListCreateAPIView):
    """
      get:
      Return a list of all the existing orders.

      post:
       Create order instance using description and itemsOrdered: [{"menuId": 1, "quantity": 2}]
       which is List of object of menu and quantity desired
    """
    queryset = Order
    serializer_class = CreateOrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        orders = Order.objects.all()
        return Response({
            "message": "success",
            "data": OrderSerializer(orders, many=True).data
        })

    def post(self, request):
        customerId = request.user
        description = request.data['description']
        orderedItems = request.data['itemsOrdered']
        orderStatus = OrderStatus.objects.create(name='P')

        amountDue = 0
        for item in orderedItems:
            menu = Menu.objects.get(id=item['menuId'])
            if item['quantity'] > menu.quantity:
                return Response({
                    'message': 'item in stock is lower than quantity requested'
                })
            menu.quantity -= item['quantity']
            menu.save()
            amountDue += menu.price * item['quantity']

        order = Order.objects.create(
            customerId=customerId, description=description,
            amountDue=amountDue,
            orderStatus=orderStatus
        )
        for item in orderedItems:
            menu = Menu.objects.get(id=item['menuId'])
            ItemsOrdered.objects.create(
                order=order, menu=menu, quantity=item['quantity'])
        return Response({
            "message": "success",
            "order": OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)


class OrderDetails(generics.RetrieveAPIView, mixins.RetrieveModelMixin):
    """
      get:
      Return an instance of order using orderId as parameter.

    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    def get_object(self, id):
        order = get_object_or_404(Order, id=id)
        return order

    def get(self, request, orderId):
        order = self.get_object(orderId)

        return Response({
            'message': 'success',
            "data": OrderSerializer(order).data
        })


class OrderPayment(generics.UpdateAPIView, mixins.UpdateModelMixin):
    """
      get:
      Return an instance of order using orderId as parameter.

      put:
      Takes in amountPaid and Update payment for orders

    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    def get_object(self, id):
        order = get_object_or_404(Order, id=id)
        return order

    def get(self, request, orderId):
        order = self.get_object(orderId)

        return Response({
            'message': 'success',
            "data":
            {
                'amountDue': order.amountDue,
                'amountPaid': order.amountPaid
            }
        })

    def put(self, request, orderId):
        # get order from database
        order = self.get_object(orderId)
        amountPaid = request.data['amountPaid']

        if order.has_paid:
            return Response({
                'message': 'Customer already paid for the order'
            }, status=status.HTTP_403_FORBIDDEN)

        order.amountPaid = amountPaid
        if order.amountOutstanding > 0:
            return Response({
                'message': 'sorry the amount paid  is lower amount of orders'
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        order.has_paid = True
        order.save()
        ordered_items = ItemsOrdered.objects.filter(order=order)
        for item in ordered_items:
            menu = Menu.objects.get(id=item.menu.id)
            vendorId = menu.vendorId.id
            subjectUser = User.objects.get(id=vendorId)
            menu_quantity = """
            Quantity: """ + str(item.quantity)
            menu_name = " Menu: " + menu.name
            message = order.customerId.email + \
                ' made ordered for the following: ' + menu_name + menu_quantity
            send_notification(subjectUser, order, message)

        return Response({
            'message': 'payment success',
            'amountDue': order.amountDue,
            'amountPaid': order.amountPaid,
            'amountOutstanding': order.amountOutstanding,
            'ordered_items': ItemListSerializer(ordered_items, many=True).data
        }, status=status.HTTP_202_ACCEPTED)


class PreOrderAPI(generics.ListCreateAPIView):
    """
      post:
      Create a new instance of preorder taking in expectedDate(), description,
      itemsOrdered: List of object that have menu and quantity desired
      eg  [{"menuId": 1, "quantity": 2}], amountPaid as request data.
    """
    queryset = PreOrder.objects.all()
    serializer_class = CreatePreorderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        customerId = request.user
        description = request.data['description']
        expectedDate = request.data['expectedDate']

        orderStatus = OrderStatus.objects.create(name='P')

        # parse date
        parse_date = datetime.strptime(expectedDate, "%Y-%m-%d").date()

        orderedItems = request.data['orderedItems']
        amount_paid = request.data['amountPaid']

        amountDue = 0
        for item in orderedItems:
            menu = Menu.objects.get(id=item['menuId'])
            if item['quantity'] > menu.quantity:
                return Response({
                    'message': 'item in stock is lower than quantity requested'
                })
            menu.quantity -= item['quantity']
            menu.save()
            amountDue += menu.price * item['quantity']

        if amount_paid < amountDue:
            return Response({
                'message': 'Amount paid is lower than total of menu purchased '
            }, status=status.HTTP_403_FORBIDDEN)
        order = PreOrder.objects.create(
            orderStatus=orderStatus,
            customerId=customerId,
            description=description,
            amountDue=amountDue,
            amountPaid=amount_paid,
            expectedDate=parse_date
        )

        for item in orderedItems:
            menu = Menu.objects.get(id=item['menuId'])
            ItemsOrdered.objects.create(
                order=order, menu=menu, quantity=item['quantity'])
            vendorId = menu.vendorId.id
            vendor = User.objects.get(id=vendorId)
            subjectUser = vendor
            menu_quantity = """ 
            Quantity: """ + str(item['quantity'])
            menu_name = " Menu: " + menu.name
            message = customerId.email + \
                ' made ordered for the following: ' + menu_name + menu_quantity
            # send notification
            send_notification(subjectUser, order, message)

        return Response({
            "message": "success",
            "data": PreorderSerializer(order).data
        }, status=status.HTTP_201_CREATED)


class CancelOrderAPI(generics.UpdateAPIView):
    """
      put:
      cancels order by orderId, 10% of amount paid is deducted for 
      inconvinence charges
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    def fine_customer(self, fine, amt_paid):
        fine_percentage = ((fine / 100) * amt_paid)
        return amt_paid - fine_percentage

    def put(self, request, orderId):
        customerId = request.user
        # get order from database
        order = get_object_or_404(Order, id=orderId)

        if order.orderStatus.name == 'C':
            return Response({
                'message': 'customer already canceled order'
            }, status=status.HTTP_403_FORBIDDEN)

        # deduct 10% from customer canceling order
        if order.has_paid:
            order.amountPaid = self.fine_customer(10, order.amountPaid)
            orderStatus = OrderStatus.objects.get(id=order.orderStatus.id)
            orderStatus.name = 'C'
            orderStatus.save()
            order.save()
            ordered_items = ItemsOrdered.objects.filter(order=order)
            for item in ordered_items:
                menu = Menu.objects.get(id=item.menu.id)
                vendorId = menu.vendorId.id
                subjectUser = User.objects.get(id=vendorId)
                menu_quantity = """
                Quantity: """ + str(item.quantity)
                menu_name = " Menu: " + menu.name
                message = order.customerId.email + \
                    ' has canceled the following orders: ' + menu_name + menu_quantity
                send_notification(subjectUser, order, message)

            return Response({
                'message': 'order cancelled successfully',
                'order': OrderSerializer(order).data
            })
        else:
            orderStatus = OrderStatus.objects.get(id=order.orderStatus.id)
            orderStatus.name = 'C'
            orderStatus.save()
            order.save()
            return Response({
                'message': 'order cancelled successfully',
                'order': OrderSerializer(order).data
            })


class VendorUpdateOrderAPI(generics.UpdateAPIView):
    """
      put:
      Update the order status and notify the customer.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsVendorOrReadOnly
    ]

    def put(self, request, orderId):
        order = get_object_or_404(Order, id=orderId)
        order_status = request.data['orderStatus']

        if order.orderStatus.name == 'C':
            return Response({
                'message': 'order has been cancelled'
            }, status=status.HTTP_403_FORBIDDEN)
        if order.has_paid == False:
            return Response({
                'message': 'order has not paid for'
            }, status=status.HTTP_403_FORBIDDEN)

        order.orderStatus.name = order_status
        order_status_name = get_status(order_status)
        order.orderStatus.save()
        order.save()
        ordered_items = ItemsOrdered.objects.filter(order=order)
        for item in ordered_items:
            menu = Menu.objects.get(id=item.menu.id)
            vendorId = menu.vendorId.id
            subjectUser = User.objects.get(id=order.customerId.id)
            message = 'Your order ' + str(order.id) + order_status_name + \
                ' find order details here....'
            send_notification(subjectUser, order, message)
        return Response({
            'message': 'order updated successfully',
            'order': OrderSerializer(order).data
        })


class DailySalesAPI(generics.GenericAPIView):
    """
      get:
      Return a list of all the sales for a particular Vendor.
        ordering from last to first instance
    """
    queryset = ItemsOrdered.objects.all()
    serializer_class = ItemOrderedSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsVendorOrReadOnly
    ]

    def get(self, request):
        vendorId = request.user
        today = datetime.now()
        todays_date = today.date()
        query = ItemsOrdered.objects.filter(
            models.Q(
                order__has_paid=True) & models.Q(dateTimeCreated=todays_date) & models.Q(menu__vendorId=vendorId))
        prices = []

        for item in query:
            prices.append(item.menu.price)
        total_sales = sum(prices)
        return Response({
            'message': 'success',
            'totalSales': total_sales,
            'itemOrdered': ItemListSerializer(query, many=True).data
        })


class NotificationAPI(generics.GenericAPIView):
    """
      get:
      Return a list of all the existing notification for a particular user.
        ordering from last to first instance
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(
            subjectUser=user).order_by('-dateTimeCreated')

        return Response({
            'message': 'success',
            'notifications': NotificationSerializer(notifications, many=True).data
        })
