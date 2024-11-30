from django.contrib import admin
from django.urls import path


from webcam import views
urlpatterns = [
    path('', views.index, name='main/Homepage'),
    path('login', views.user_login, name='main/login'),
    path('about', views.about, name='main/about'),
    path('contact', views.contact, name='main/contact'),
    path('dashboard', views.dashboard, name='main/dashboard'),
    path('live_stream', views.livestream, name='main/live_stream'),
    path('employee_main', views.employee_main, name='main/employee'),
    path('admin_main', views.admin_main, name='main/admin_main'),
    path('update_employee/<int:account_id>', views.update_employee, name='main/update_employee'),
    path('add_employee', views.add_employee, name='main/add_employee'),
    path('delete_account/<int:account_id>', views.delete_account, name='main/delete_account'),
    path('admin_all',views.admin_all, name='main/admin_all'),
    path('video_feed/', views.video_feed, name='video_feed'),

]