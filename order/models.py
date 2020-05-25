from django.db import models
from accounts.models import User, Vendor, Customer
from menu.models import Menu
# Create your models here.


class OrderStatus(models.Model):
    CHOICES = (
        ('P', 'Proccesing'),
        ('T', 'In-Transit'),
        ('C', 'Canceled'),
        ('D', 'Delivered')
    )
    name = models.CharField(max_length=1, choices=CHOICES, default='B')

    def __str__(self):
        return (self.name)


class Order(models.Model):
    customerId = models.ForeignKey(
        User, related_name='custsomer',  on_delete=models.CASCADE)
    description = models.TextField()
    amountPaid = models.FloatField(blank=True, null=True)
    orderStatus = models.ForeignKey(
        OrderStatus, on_delete=models.CASCADE)
    dateAndTimeOfOrder = models.DateTimeField(auto_now_add=True)
    amountDue = models.FloatField(blank=True, null=True)
    has_paid = models.BooleanField(default=False)
    itemsOrdered = models.ManyToManyField(
        Menu, through='ItemsOrdered')
    dateTimeCreated = models.DateTimeField(auto_now_add=True)

    @property
    def amountOutstanding(self):
        return float(self.amountDue - self.amountPaid)


class ItemsOrdered(models.Model):
    menu = models.ForeignKey(Menu, related_name='menus',
                             on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    dateTimeCreated = models.DateField(auto_now_add=True)


class MessageStatus(models.Model):
    CHOICES = (
        ('S', 'Sent'),
        ('D', 'Delivered'),
        ('R', 'Read')
    )
    name = models.CharField(choices=CHOICES, max_length=1, default=None)

    def __str__(self):
        return (self.name)


class Notification(models.Model):
    subjectUser = models.ForeignKey(User, on_delete=models.CASCADE)
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    messageStatus = models.ForeignKey(MessageStatus, on_delete=models.CASCADE)
    dateTimeCreated = models.DateTimeField(auto_now_add=True)


class PreOrder(Order):
    expectedDate = models.DateField(auto_now_add=False)

    REQUIRED_FIELDS = ['customerId',
                       'expectedDate', 'orderStatus', 'amountPaid']

    def __str__(self):
        return self.expectedDate
