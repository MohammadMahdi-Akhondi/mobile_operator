from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError
from spyne.error import ResourceNotFoundError, ResourceAlreadyExistsError
from spyne.util.django import DjangoComplexModel
from spyne.model.primitive import Integer
from spyne.model.fault import Fault
from spyne.service import Service
from spyne.decorator import rpc
from datetime import date

from ..models import Subscriber


class SubscriberData(DjangoComplexModel):
    """
    A DjangoComplexModel class for representing subscriber data.

    This class extends the DjangoComplexModel class and represents subscriber data
    as a complex type in a SOAP web service. It maps to the Subscriber model in the
    Django application.
    """
    class Attributes(DjangoComplexModel.Attributes):
        django_model = Subscriber


class SubscriberService(Service):
    """
    A SOAP web service for managing subscribers.

    This service provides two methods for managing subscribers: `get_subscriber`
    and `create_subscriber`. The `get_subscriber` method retrieves a subscriber
    by its primary key, and the `create_subscriber` method creates a new subscriber.
    """
    @rpc(Integer, _returns=SubscriberData)
    def get_subscriber(ctx, pk):
        """
        Retrieve a subscriber by its primary key.

        :param pk (int): The primary key of the subscriber to retrieve.
        :returns: SubscriberData: The subscriber data for the specified primary key.
        :raises: ResourceNotFoundError: If the specified subscriber does not exist.
        """
        try:
            return Subscriber.objects.get(pk=pk)

        except Subscriber.DoesNotExist:
            raise ResourceNotFoundError('Subscriber')

    @rpc(SubscriberData, _returns=SubscriberData)
    def create_subscriber(ctx, subscriber):
        """
        Create a new subscriber.

        :param subscriber (SubscriberData): The subscriber data to create.
        :returns: SubscriberData: The newly created subscriber data.
        :raises: Fault: If the subscriber has not reached legal age.
        :raises: ResourceAlreadyExistsError: If a subscriber with the same national code already exists.
        """
        if not is_legal_age(subscriber.birthdate):
            raise Fault(
                faultcode='The subscriber has not reached legal age',
                faultstring='The minimum age for subscriber registration is 18 years.',
            )

        try:
            return Subscriber.objects.create(**subscriber.as_dict())

        except IntegrityError:
            raise ResourceAlreadyExistsError('Subscriber')


def is_legal_age(birthdate: date) -> bool:
    LEGAL_AGE = 18
    today = date.today()
    age = today.year - birthdate.year - \
        ((today.month, today.day) < (birthdate.month, birthdate.day))
    return True if age >= LEGAL_AGE else False
