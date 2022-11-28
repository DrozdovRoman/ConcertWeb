"""workproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('concert', views.ConcertCreateView.as_view(), name='concert'),
    path('update-concertPage/<int:pk>',views.ConcertUpdateView.as_view(), name='update_concert_page'),
    path('delete-concertPage/<int:pk>',views.delete_concert_page, name='delete_concert_page'),
    path('sell', views.SellCreateView.as_view(), name='sell'),
    path('update-sellPage/<int:pk>',views.SellUpdateView.as_view(), name='update_sell_page'),
    path('delete-sellPage/<int:pk>',views.delete_sell_page, name='delete_sell_page'),
    path('target', views.TargetCreateView.as_view(), name='target'),
    path('update-targetPage/<int:pk>',views.TargetUpdateView.as_view(), name='update_target_page'),
    path('delete-targetPage/<int:pk>',views.delete_target_page, name='delete_target_page'),
]