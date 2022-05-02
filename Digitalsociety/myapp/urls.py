"""Digitalsociety URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
     path('', views.home, name='home'), 
     path('login/', views.login, name='login'),

     path('watchman-registration/', views.watchman_registration, name='watchman-registration'),
     path('watchman-approval/', views.watchman_approval, name='watchman-approval'),
     path('logout/', views.logout, name='logout'),

     path('profile/', views.profile, name='profile'),
     path('change-password/', views.change_password, name='change-password'),

     path('add-member/', views.add_member, name='add-member'),
     path('view-member/', views.view_member, name='view-member'),
     path('m-view-profile/<int:pk>', views.m_view_profile, name='m-view-profile'),
     path('m-delete-profile/<int:pk>', views.m_delete_profile, name='m-delete-profile'),
     path('m-edit-profile/<int:pk>', views.m_edit_profile, name='m-edit-profile'),
     path('m-update-profile', views.m_update_profile, name='m-update-profile'),

    path('add-event/', views.add_event, name='add-event'),
    path('view-event/', views.view_event, name='view-event'),
    path('edit-event/<int:ek>', views.edit_event, name='edit-event'),
    path('update-event/', views.update_event, name='update-event'),
    path('delete-event/<int:ek>', views.delete_event, name='delete-event'),

    path('add-notice/', views.add_notice, name='add-notice'),
    path('view-notice', views.view_notice, name='view-notice'),
    path('delete-notice/<int:nk>', views.delete_notice, name='delete-notice'),
    
    path('add-photos/', views.add_photos, name='add-photos'), 
    path('view-photos/', views.view_photos, name='view-photos'), 
    path('delete-photos/<int:pk>', views.delete_photos, name='delete-photos'),

    path('add-video/', views.add_video, name='add-video'),
    path('view-video/', views.view_video, name='view-video'),
    path('delete-video/<int:pk>', views.delete_video, name='delete-video'),

    path('add-suggestion/', views.add_suggestion, name='add-suggestion'),
    path('view-suggestion/', views.view_suggestion, name='view-suggestion'),
    path('delete-suggestion/<int:sk>', views.delete_suggestion, name='delete-suggestion'),

    path('add-rentsell-request/', views.add_rentsell_request, name='add-rentsell-request'),
    path('view-rentsell-request/', views.view_rentsell_request, name='view-rentsell-request'),

    path('view-rentsell-all-request/', views.view_rentsell_all_request, name='view-rentsell-all-request'),
    path('view-rentsell-request-details/<int:pk>', views.view_rentsell_request_details, name='view-rentsell-request-details'),
    path('delete-rentsell-request/<int:pk>',views.delete_rentsell_request,name='delete-rentsell-request'),

    path('add-maintenance/', views.add_maintenance, name='add-maintenance'),
    path('view-maintenance/', views.view_maintenance, name='view-maintenance'),
    path('delete-maintenance/<int:pk>',views.delete_maintenance,name='delete-maintenance'),

]
