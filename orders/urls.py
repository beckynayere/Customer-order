# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import (
    ProductView,
    HomeView,
    OrderDetailView,
    ItemListView,
    ItemDetailView,
    AddToCartView,
    OrderItemDeleteView,
    OrderQuantityUpdateView
)

app_name = 'orders'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('detail_profile/', views.detail_profile, name='detail_profile'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('customers/', CustomerView.as_view(), name='add-customer'),
    path('orders/', OrderView.as_view(), name='add-order'),
    path('', HomeView.as_view(), name='home'),
    path('product/<int:pk>/', ProductView.as_view(), name='product'),
    path('product-list/', views.product_list, name='product_list'),
    path('search/', views.product_search, name='product_search'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('products/', ItemListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ItemDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    
    path('order-summary/', OrderDetailView.as_view(), name='order-summary'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('order-items/<int:pk>/delete/', OrderItemDeleteView.as_view(), name='order-item-delete'),
    path('order-item/update-quantity/', OrderQuantityUpdateView.as_view(), name='order-item-update-quantity'),
    path('create/', views.order_create, name='order_create'),
    path('process/', views.order_save, name='order_save'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
