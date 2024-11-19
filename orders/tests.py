from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Customer, Order

class CustomerOrderTests(APITestCase):

    def setUp(self):
        self.customer_data = {"name": "John Doe", "code": "C123"}
        self.order_data = {"item": "Laptop", "amount": 1000, "time": "2024-11-19T12:00:00", "customer": 1}

    def test_add_customer(self):
        response = self.client.post(reverse('add-customer'), self.customer_data)
        self.assertEqual(response.status_code, 201)

    def test_add_order(self):
        customer = Customer.objects.create(**self.customer_data)
        self.order_data['customer'] = customer.id
        response = self.client.post(reverse('add-order'), self.order_data)
        self.assertEqual(response.status_code, 201)

