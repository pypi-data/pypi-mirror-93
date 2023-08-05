from django.urls import path, re_path

#from .views import  *
from . import views

urlpatterns = [
   
    #last device/add activity
    path('listagem/', views.ListConectividadeView.as_view(), name='list'),
    path('addactivity/',views.CreateactivityView.as_view(), name= 'addactivity'),   


    #Activity Filter URLs
    # Activity URLs
    path('activityop/', views.ActivityopListView.as_view(), name='activity_op_list'),#página inicial: permite escolha da listagem
    path('activity/', views.ActivityListView.as_view(), name='activity_list'),#old
    path('activity/install/', views.ActivityListView.as_view(), {'type': 'INSTALL'}, name='activity_install_list', ),
    path('activity/remove/', views.ActivityListView.as_view(), {'type': 'REMOVE'}, name='activity_remove_list'),

    path('activitydetails/<int:pk>/', views.ActivityDetailsView.as_view(), name='activity_details'),
    path('activitydetails/update/<int:atv>', views.ActivityUpdateView.as_view(), name='activity_update'),

    #device
    path('device_addactivity/', views.DeviceHistoryView.as_view(), name='device_addactivity'),

    path('device/<int:pk>/', views.DeviceHistoryView.as_view(), name='device_history'),
    
    #multiple Device
    path('device_select_multiple_devices/', views.SelectMultipleView.as_view(), name='device_select_multiple_devices'),
    #path('device_add_multiple_activity/', views.DeviceMultipleView.as_view(), name='device_add_multiple_activity'),



    #Actor
   
    path('addactor/', views.CreateActor.as_view(), name='addactor'),

    path('<int:pk>/', views.ActorView.as_view(), name='actor'),

    path('<int:pk>/edit/', views.EditActor.as_view(), name='actor_edit'),

    path('<int:pk>/delete/', views.DeleteActor.as_view(), name='actor_delete'),

    path('delete/', views.BulkDeleteActor.as_view(), name='actor_bulk_delete'),

    path('actor_list/', views.ActorListView.as_view(), name='actor_list'),
    
    
    #search device
    path('searchdevice/', views.ListDeviceView.as_view(), name='searchdevice'),
    path('searchdeviceresult/', views.SearchDeviceView.as_view(), name='searchdeviceresult'),
]