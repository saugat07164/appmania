from django.conf import settings
from django.urls import path
from . import views  # Import the views module
from .views import ItemListView, ItemDetailView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('home/', views.home_view, name='home_view'),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),

]

# Include static and media URL patterns for debug mode
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
