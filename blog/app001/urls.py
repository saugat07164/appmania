from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home_view'),
    path('add/', views.create_post, name='add_view'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('money/', views.mon_view, name='mon_view'),
    path('inc/', views.create_income, name='create_income'),
    path('exp/', views.create_expense, name='create_expense'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('download_statement', views.download_st, name='download_st'), 
]

# Include static and media URL patterns for debug mode
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
