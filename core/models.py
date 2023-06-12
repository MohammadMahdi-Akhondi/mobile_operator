from django.utils.translation import gettext_lazy as _
from django.db import models


class Subscriber(models.Model):
    """
    Subscriber model used to store user information.

    This model represents a subscriber and includes fields for their ID, first
    name, last name, national code, father name, Shenasname ID, birthdate, and
    address.
    """
    id = models.IntegerField(
        primary_key=True,
        editable=False,
        verbose_name=_('ID')
    )
    first_name = models.CharField(
        max_length=200,
        verbose_name=_('First name')
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name=_('Last name')
    )
    national_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('National code')
    )
    father_name = models.CharField(
        max_length=200,
        verbose_name=_('Father name')
    )
    shenasname_id = models.CharField(
        max_length=10,
        verbose_name=_('Shenasname id')
    )
    birthdate = models.DateField(
        verbose_name=_('Birth day')
    )
    address = models.TextField(
        verbose_name=_('Address')
    )

    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')
    
    def __str__(self) -> str:
        return self.first_name


class MobileLine(models.Model):
    """
    MobileLine model used to store the information of a mobile phone line.

    This model represents a mobile phone line and its associated subscriber. It
    includes fields for the line's ID, name, phone number, and subscriber ID.
    """
    id = models.IntegerField(
        primary_key=True,
        editable=False,
        verbose_name=_('ID')
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_('Name')
    )
    number = models.CharField(
        max_length=11,
        unique=True,
        verbose_name=_('Number')
    )
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name='mobile_lines',
        verbose_name=_('Subscriber')
    )

    class Meta:
        verbose_name = _('Mobile line')
        verbose_name_plural = _('Mobile line')
    
    def __str__(self) -> str:
        return self.name
