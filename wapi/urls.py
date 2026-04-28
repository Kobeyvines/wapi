"""
URL configuration for wapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from events.views import EventViewSet, CategoryViewSet, BookingViewSet
from accounts.views import UserViewSet
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.shortcuts import redirect
# Ensure initiate_payment and mpesa_callback are imported here!
from events.views import (
    EventViewSet, 
    CategoryViewSet, 
    BookingViewSet, 
    initiate_payment, 
    mpesa_callback
)
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'accounts', UserViewSet, basename='user')
router.register(r'bookings', BookingViewSet, basename='booking')


urlpatterns = [
    
    path('admin/', admin.site.urls),
    
    # Include all our API endpoints under the 'api/' prefix
    path('api/', include(router.urls)),
    
    # 1. The Schema (The "Source of Truth" for your API)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Swagger UI (The Interactive Testing Lab)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # 3. Redoc (A cleaner, read-only documentation view)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Redirect root to docs
    path('', lambda request: __import__('django.shortcuts').shortcuts.redirect('api/docs/', permanent=False)),
    # 5. MPESA
    path('api/payments/initiate/<uuid:booking_id>/', initiate_payment, name='initiate-payment'),
    
    path('api/payments/callback/', mpesa_callback, name='mpesa-callback'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)