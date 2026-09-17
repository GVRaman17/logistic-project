from django.urls import path
from . import views
urlpatterns = [
    path('',views.mainlogin,name='mainlogin'),
    path('admindashboard/<int:id>/',views.admindashboard,name='admindashboard'),
    path('success/',views.success,name='success'),
    path('loginprocess/',views.loginprocess,name='loginprocess'),
    path('registration/',views.registration,name='registration'),
    path('registrationprocess/',views.registrationprocess,name='registrationprocess'),
    path('admindashboard/adddriver/<int:id>/',views.adddriver,name='adddriver'),
    path('admindashboard/addlocation/<int:id>/',views.addlocation,name='addlocation'),
    path('customerdashboard/<int:id>/',views.customerdashboard,name='customerdashboard'),
    path('customerdashboard/ordering/<int:id>/',views.ordering,name='ordering'),
    path('admindashboard/assingdriver/<int:id>/',views.assingdriver,name='assingdriver'),
    path('driverdashboard/<int:id>/',views.driverdashboard,name='driverdashboard'),
    path('driverdashboard/delivered/<int:orderid>/<int:driverid>/',views.delivered,name='delivered'),
    path('logout/', views.logout, name='logout'),
    path('duplicatename/',views.duplicatename,name='duplicatename')


]
