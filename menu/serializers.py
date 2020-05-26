from rest_framework import serializers
from .models import Menu
from accounts.models import Vendor, Customer, User


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'email', 'phone_number', 'business_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'isVendor']


class MenuSerializers(serializers.ModelSerializer):
    vendorId = UserSerializer(read_only=True)
    name = serializers.CharField(
        min_length=100,
        help_text="string: Name of the menu"
    )
    description = serializers.CharField(
        help_text="textfield: Description of the menu"
    )
    price = serializers.FloatField(
        help_text="float: Price per plate"
    )
    quantity = serializers.IntegerField(
        help_text="int: Quantity available"
    )
    isRecurring = serializers.BooleanField(
        help_text="bool: is it a Recurring order"
    )
    frequencyOfReocurrence = serializers.ChoiceField(
        choices=[
            ('E', 'Everyday'),
            ('M', 'Mondays'),
            ('T', 'Tuesdays'),
            ('W', 'Wednesdays'),
            ('TH', 'Thursdays'),
            ('F', 'Fridays'),
            ('WK', 'Weeekends')
        ],
        help_text="""choices: E = Everyday, M=Mondays, T = Tuesdays, 
        W = Wednesday, TH = Thursdays, F = Fridays,
        WK = Weekends
        """
    )

    class Meta:
        model = Menu
        fields = '__all__'
        depth = 1


class MenuCreateSerializers(serializers.ModelSerializer):
    name = serializers.CharField(
        min_length=100,
        help_text="string: Name of the menu"
    )
    description = serializers.CharField(
        help_text="textfield: Description of the menu"
    )
    price = serializers.FloatField(
        help_text="float: Price per plate"
    )
    quantity = serializers.IntegerField(
        help_text="int: Quantity available"
    )
    isRecurring = serializers.BooleanField(
        help_text="bool: is it a Recurring order"
    )
    frequencyOfReocurrence = serializers.ChoiceField(
        choices=[
            ('E', 'Everyday'),
            ('M', 'Mondays'),
            ('T', 'Tuesdays'),
            ('W', 'Wednesdays'),
            ('TH', 'Thursdays'),
            ('F', 'Fridays'),
            ('WK', 'Weeekends')
        ],
        help_text="""choices: E = Everyday, M=Mondays, T = Tuesdays, 
        W = Wednesday, TH = Thursdays, F = Fridays,
        WK = Weekends
        """
    )

    class Meta:
        model = Menu
        fields = ['name', 'description', 'price', 'quantity',
                  'isRecurring', 'frequencyOfReocurrence']
        depth = 1
