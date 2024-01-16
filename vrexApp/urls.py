from django.urls import path

from . import views
    
urlpatterns = [
  
  path('',views.home, name=""),
  path('register', views.register, name="register"),
  path('login', views.login, name="login"),
  path('logout', views.logout, name="logout"),
  path('dashboard', views.dashboard, name="dashboard"),
  path('announcement', views.announcement, name="announcement"),
  path('formrequest', views.formrequest, name="formrequest"),
  path('checkstatus', views.checkstatus, name="checkstatus"),
  path('calendar', views.calendar, name="calendar"),
  path('chat', views.chat, name="chat"),
  path('financial', views.financial, name="financial"),
  
]
