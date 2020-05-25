from rest_framework import serializers
from .models import Order, OrderStatus, PreOrder, ItemsOrdered, Notification
from accounts.models import Customer
from menu.serializers import MenuSerializers


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'email', 'first_name', 'last_name']


class OrderStatusSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(
        choices=(
            ('P', 'Proccesing'),
            ('T', 'In-Transit'),
            ('C', 'Canceled'),
            ('D', 'Delivered')
        ),
        help_text="""
            P = Proccesing, T = In-Transit, C = Canceled,
            D = Delivered
        """
    )

    class Meta:
        model = OrderStatus
        fields = ['id', 'name']


class ItemOrderedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsOrdered
        fields = ['menu', 'quantity']


class ItemListSerializer(serializers.ModelSerializer):
    menu = MenuSerializers(read_only=True)

    class Meta:
        model = ItemsOrdered
        fields = ['menu', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    orderStatus = OrderStatusSerializer()

    class Meta:
        model = Order
        fields = [
            'id',
            'description',
            'orderStatus',
            'amountDue',
            'amountPaid',
            'itemsOrdered',
            'dateAndTimeOfOrder'
        ]
        depth = 1


class CreateOrderSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        help_text='Additional info about the orders'
    )
    itemsOrdered = serializers.ListField(
        child=ItemOrderedSerializer(many=True),
        help_text='List of object that have menu and quantity desired eg [{"menuId": 1, "quantity": 2}]'
    )

    class Meta:
        model = Order
        fields = [
            'description',
            'itemsOrdered',
        ]


class CreatePreorderSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        help_text='Additional info about the orders'
    )
    itemsOrdered = serializers.ListField(
        child=ItemOrderedSerializer(many=True),
        help_text='List of object that have menu and quantity desired eg [{"menuId": 1, "quantity": 2}]'
    )
    expectedDate = serializers.DateField(
        help_text='Date Expected to deliver the order'
    )
    amountPaid = serializers.FloatField(
        help_text='Total amount of the menu'
    )

    class Meta:
        model = Order
        fields = [
            'description',
            'itemsOrdered',
            'expectedDate',
            'amountPaid'
        ]


class PreorderSerializer(serializers.ModelSerializer):
    orderStatus = OrderStatusSerializer()
    customer = CustomerSerializer(read_only=True)
    itemsOrdered = ItemOrderedSerializer(many=True, read_only=True)

    class Meta:
        model = PreOrder
        fields = [
            'id',
            'customer',
            'expectedDate',
            'description',
            'orderStatus',
            'amountDue',
            'amountPaid',
            'itemsOrdered',
            'dateAndTimeOfOrder'
        ]
        depth = 1


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
