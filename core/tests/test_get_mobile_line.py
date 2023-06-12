from django.test import TestCase
from django.urls import reverse_lazy
from spyne.client.django import DjangoTestClient
from datetime import date

from ..models import Subscriber, MobileLine
from ..urls import app


class MobileLineTestCase(TestCase):
    """
    A Django test case for testing the MobileLine model and SOAP web service.

    This test case provides methods for testing the `get_mobile_line` and
    `create_mobile_line` methods of the SOAP web service for the MobileLine model.
    It sets up a test client using the DjangoTestClient class and creates a
    Subscriber and MobileLine object for testing.
    """
    def setUp(self):
        self.url = reverse_lazy('soap_service')
        self.client = DjangoTestClient(self.url, app)
        self.subscriber = Subscriber.objects.create(
            id=1, first_name='mahdi', last_name='akhondi',
            national_code='0123456249', father_name='dad',
            shenasname_id='0123456249', address='tehran',
            birthdate=date(year=1990, month=6, day=16),
        )
        self.mobile_line = MobileLine.objects.create(
            id=1, name='first', number='051556', subscriber=self.subscriber
        )

    def test_valid_get_mobile_line(self):
        pk = self.mobile_line.id
        response = self.client.service.get_mobile_line(pk)
        self.assertEqual(
            response.id,
            pk,
        )

    def test_response_encoding_get_mobile_line(self):
        pk = self.subscriber.id
        response = self.client.service.get_mobile_line.get_django_response(pk)
        self.assertTrue('Content-Type' in response)
        self.assertTrue(response['Content-Type'].startswith('text/xml'))

    def test_valid_create_mobile_line(self):
        data = {
            'name': 'first', 'number': '0515568', 'subscriber_id': 1,
        }
        response = self.client.service.create_mobile_line.get_django_response(data)
        self.assertEqual(
            response.status_code,
            200,
        )

    def test_response_encoding_create_mobile_line(self):
        pk = self.subscriber.id
        response = self.client.service.create_mobile_line.get_django_response(pk)
        self.assertTrue('Content-Type' in response)
        self.assertTrue(response['Content-Type'].startswith('text/xml'))
