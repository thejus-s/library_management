from django.urls import path
from . import views

urlpatterns = [
    path('admindashboard/',views.admindash,name='admindash'),
    path('adminviewbooks/',views.adminallbooks,name='viewbooks'),
    path('addbooks/',views.addbooks,name='addbooks'),
    path('adminsearch/',views.adminsearchbook,name='adminsearch'),
    path('editbook/<slug:slug>',views.editbook,name='editbook'),
    path('overduebooks',views.overduebooks,name='overdue'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('deletebook/<slug:slug>',views.deletebook,name='deletebook'),
    path('deleteuser/<int:id>',views.deleteuser,name='deleteuser'),
]