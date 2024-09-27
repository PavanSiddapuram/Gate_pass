# mypass/urls.py

from django.urls import path
from . import views



urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('returnable_form/', views.returnable_form_view, name='returnable_form'),
    path('nonreturnable_form/', views.nonreturnable_form_view, name='nonreturnable_form'),
    path('approval/', views.approval_view, name='approval'),
    path('activity/', views.activity_view, name='activity'),
    path('print_request/<int:id>/', views.print_request_view, name='print_request'),
    path('request/<int:pk>/', views.request_details, name='request_details'),
    path('view_details/<int:gate_pass_id>/', views.view_details_view, name='view_details'),  # Added URL pattern

]



