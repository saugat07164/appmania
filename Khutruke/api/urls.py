from django.conf import settings
from django.urls import path
from . import views  # Import the views module
from .views import ItemListAPIView, ItemDetailAPIView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('itemsapi/', ItemListAPIView.as_view(), name='item-list-api'),
    path('itemsapi/<int:pk>/', ItemDetailAPIView.as_view(), name='item-detail-api'),
   

]

# Include static and media URL patterns for debug mode
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
