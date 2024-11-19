# orders/views.py
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Order, Product, OrderItem
from .models import Profile
from .serializers import OrderSerializer
from .africastalking_config import sms
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CustomerSerializer, 
    OrderSerializer, 
    ProductSerializer, 
   
)

# View to handle customer-related operations (ViewSet for CRUD)
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

# Custom APIView for additional customer functionality
class CustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to handle product-related operations
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

# ViewSet for order-related operations with custom create logic
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Custom order creation logic (e.g., sending SMS or notifications)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        # Add your SMS or notification logic here
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Custom APIView for additional order functionality
from .models import Customer, Order
from .serializers import OrderSerializer
from .africastalking_config import sms

class OrderView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['write']

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # Retrieve the customer's phone number
            customer = order.customer
            phone_number = customer.phone_number

            # Send SMS
            message = f"Hi {customer.name}, your order for {order.item} has been placed successfully!"
            try:
                sms.send(message, [phone_number])
                return Response(
                    {"message": "Order created and SMS sent successfully!", "order": serializer.data},
                    status=201,
                )
            except Exception as e:
                return Response(
                    {"error": f"Order created but SMS failed: {str(e)}", "order": serializer.data},
                    status=201,
                )
        return Response(serializer.errors, status=400)

# ViewSet for handling order items
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated]

