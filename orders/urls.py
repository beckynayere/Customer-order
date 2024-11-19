from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCLogoutView
from oauth2_provider.urls import urlpatterns as oauth2_urls

from . import views
from .views import (
    CustomerView,
    OrderView,
    
)

# DRF router for API endpoints
router = DefaultRouter()
router.register(r'api/customers', views.CustomerViewSet, basename='customer')
router.register(r'api/products', views.ProductViewSet, basename='product')
router.register(r'api/orders', views.OrderViewSet, basename='order')
router.register(r'api/order-items', views.OrderItemViewSet, basename='order-item')

app_name = 'orders'

urlpatterns = [
    # Authentication routes
    path('', include('django.contrib.auth.urls')),
    path('openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    path('oauth/', include(oauth2_urls)),
    path('oidc/authenticate/', OIDCAuthenticationRequestView.as_view(), name='oidc_authenticate'),
    path('oidc/logout/', OIDCLogoutView.as_view(), name='oidc_logout'),
    path('oidc/', include('mozilla_django_oidc.urls')),
    # path('detail_profile/', views.detail_profile, name='detail_profile'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Template-based views
    # path('', HomeView.as_view(), name='home'),
    # path('product/<int:pk>/', ProductView.as_view(), name='product'),
    # path('product-list/', views.product_list, name='product_list'),
    # path('search/', views.product_search, name='product_search'),
    # path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    # path('products/', ItemListView.as_view(), name='product-list'),
    # path('products/<int:pk>/', ItemDetailView.as_view(), name='product-detail'),
    # path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    # path('order-summary/', OrderDetailView.as_view(), name='order-summary'),
    # path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # Order item management
    # path('order-items/<int:pk>/delete/', OrderItemDeleteView.as_view(), name='order-item-delete'),
    # path('order-item/update-quantity/', OrderQuantityUpdateView.as_view(), name='order-item-update-quantity'),

    # Custom order routes
    # path('create/', views.order_create, name='order_create'),
    # path('process/', views.order_save, name='order_save'),

    # API views
    path('api/customers/custom/', CustomerView.as_view(), name='add-customer'),
    path('api/orders/custom/', OrderView.as_view(), name='add-order'),
    path('api/', include(router.urls)),  # Include router-generated API routes
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
