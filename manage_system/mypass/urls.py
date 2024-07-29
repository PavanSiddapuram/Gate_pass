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
    path('forgot_password/', views.forgot_view, name='forgot_password'),
]
