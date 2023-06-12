from django.test import TestCase
from django.urls import reverse_lazy
from spyne.client.django import DjangoTestClient
from datetime import date

from ..models import Subscriber
from ..urls import app


class SubscriberTestCase(TestCase):
    """
    A Django test case for testing the Subscriber model and SOAP web service.

    This test case provides methods for testing the `get_subscriber` and
    `create_subscriber` methods of the SOAP web service for the Subscriber model.
    It sets up a test client using the DjangoTestClient class and creates a
    Subscriber object for testing.
    """
    def setUp(self):
        self.url = reverse_lazy('soap_service')
        self.client = DjangoTestClient(self.url, app)
        self.subscriber = Subscriber.objects.create(
            id=1, first_name='mahdi', last_name='akhondi',
            national_code='0123456789', father_name='dad',
            shenasname_id='0123456789', address='tehran',
            birthdate=date(year=1990, month=6, day=16),
        )

    def test_valid_get_subscriber(self):
        pk = self.subscriber.id
        response = self.client.service.get_subscriber(pk)
        self.assertEqual(
            response.id,
            pk,
        )

    def test_response_encoding_get_subscriber(self):
        pk = self.subscriber.id
        response = self.client.service.get_subscriber.get_django_response(pk)
        self.assertTrue('Content-Type' in response)
        self.assertTrue(response['Content-Type'].startswith('text/xml'))

    def test_valid_create_subscriber(self):
        data = {
            'first_name': 'ali', 'last_name': 'ahmadi',
            'national_code': '4567891230', 'father_name': 'father',
            'shenasname_id': '4567891230', 'address': 'tehran',
            'birthdate': date(year=1990, month=5, day=10),
        }
        response = self.client.service.create_subscriber.get_django_response(data)
        self.assertEqual(
            response.status_code,
            200,
        )

    def test_response_encoding_create_subscriber(self):
        pk = self.subscriber.id
        response = self.client.service.create_subscriber.get_django_response(pk)
        self.assertTrue('Content-Type' in response)
        self.assertTrue(response['Content-Type'].startswith('text/xml'))
