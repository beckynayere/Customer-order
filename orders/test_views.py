from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customer, Order
from .africastalking_config import sms

class CustomerOrderTestCase(APITestCase):

    def setUp(self):
        # Create a customer for testing
        self.customer = Customer.objects.create(name="John Doe", code="C123", phone_number="+254711123456")
        self.order_data = {
            "customer": self.customer.id,
            "item": "Laptop",
            "amount": 1200.50
        }

    def test_create_order(self):
        # Test creating an order
        response = self.client.post("/api/orders/", self.order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sms_sent_on_order(self):
        # Mock the SMS sending function
        def mock_send(message, recipients):
            return {"SMSMessageData": {"Recipients": [{"status": "Success"}]}}

        sms.send = mock_send

        response = self.client.post("/api/orders/", self.order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Order created and SMS sent successfully!", response.data["message"])
