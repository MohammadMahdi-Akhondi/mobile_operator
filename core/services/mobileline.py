from django.db.utils import IntegrityError
from spyne.error import ResourceNotFoundError, ResourceAlreadyExistsError
from spyne.util.django import DjangoComplexModel
from spyne.model.primitive import Integer
from spyne.model.fault import Fault
from spyne.service import Service
from spyne.decorator import rpc

from ..models import MobileLine


class MobileLineData(DjangoComplexModel):
    """
    A `DjangoComplexModel` used to map the `MobileLine` model to XML.

    `DjangoComplexModel` is a base class for defining complex models in `spyne`
    that are based on Django models. It enables automatic conversion of Django
    models to XML or JSON formats for use in SOAP web services.
    """
    class Attributes(DjangoComplexModel.Attributes):
        django_model = MobileLine


class MobileLineService(Service):
    """
    A SOAP web service for managing mobile lines.

    This service provides two methods for managing mobile lines: `get_mobile_line`
    and `create_mobile_line`. The `get_mobile_line` method retrieves a mobile line
    by its primary key, and the `create_mobile_line` method creates a new mobile line.
    """
    @rpc(Integer, _returns=MobileLineData)
    def get_mobile_line(ctx, pk):
        """
        Retrieve a mobile line by its primary key.

        :param pk (int): The primary key of the mobile line to retrieve.
        :returns: MobileLineData: The mobile line data for the specified primary key.
        :raises: ResourceNotFoundError: If the specified mobile line does not exist.
        """
        try:
            return MobileLine.objects.get(pk=pk)

        except MobileLine.DoesNotExist:
            raise ResourceNotFoundError('MobileLine')

    @rpc(MobileLineData, _returns=MobileLineData)
    def create_mobile_line(ctx, mobile_line):
        """
        Create a new mobile line.

        :param mobile_line (MobileLineData): The mobile line data to create.
        :returns: MobileLineData: The newly created mobile line data.
        :raises: Fault: If the subscriber has exceeded the maximum number of mobile lines.
        :raises: ResourceAlreadyExistsError: If a mobile line with the same number already exists.
        """
        if not valid_line_counts(mobile_line.subscriber_id):
            raise Fault(
                faultcode='Too many mobile lines',
                faultstring='The maximum number of mobile line registration for each subscriber is 10.',
            )

        try:
            return MobileLine.objects.create(**mobile_line.as_dict())

        except IntegrityError:
            raise ResourceAlreadyExistsError('MobileLine')


def valid_line_counts(subscriber_id: int) -> bool:
    """
    Check if the number of mobile lines for a subscriber is less than the limit.

    :param subscriber_id (int): The ID of the subscriber.
    :returns: bool: True if the subscriber has not exceeded the maximum number of mobile lines, False otherwise.
    """
    LINE_COUNT_LIMIT = 10
    if MobileLine.objects.filter(subscriber__id=subscriber_id).count() < LINE_COUNT_LIMIT:
        return True
    return False
