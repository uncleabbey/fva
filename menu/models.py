from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import Vendor, Customer


# Create your models here.
class Menu(models.Model):

  FREQUENCY =(
    ('D', 'Daily'),
    ('B', 'Bi-Weekly'),
    ('W', 'Weekly'),
    ('E', 'Weeekend')
  )  

  name = models.CharField(_("Name"), max_length=50)
  description = models.TextField(_("Description"))
  price = models.FloatField(default=0.00)
  quantity = models.IntegerField()
  dateTimeCreated = models.DateTimeField(_("Date Created"), auto_now_add=True)
  vendorId = models.ForeignKey(Vendor, verbose_name=_("vendor"), on_delete=models.CASCADE)
  isRecurring = models.BooleanField(default=False)
  frequencyOfReocurrence = models.CharField(_("Frequency"), choices=FREQUENCY, default=None, max_length=1)
  img_url = models.CharField(_("Image"), max_length=100, blank=True, null=True, default=None)
  