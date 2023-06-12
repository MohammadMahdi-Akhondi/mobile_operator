from django.urls import path
from spyne.server.django import DjangoView
from spyne.application import Application
from spyne.protocol.soap import Soap11

from .services import subscriber, mobileline


# SOAP application
app = Application(
    [
        subscriber.SubscriberService,
        mobileline.MobileLineService,
    ],
    tns='soap.service.core',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)

urlpatterns = [
    path('', DjangoView.as_view(application=app), name='soap_service'),
]
