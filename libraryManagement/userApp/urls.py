from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('search/',views.searchbook,name='search'),
    path('profile/',views.userprofile,name='profile'),
    path('borrow/<slug:slug>',views.borrow,name='borrow'),
    path('return/<int:bid>',views.returnbook,name='return'),
    path('allbooks/',views.allbooks,name='allbooks'),
    path('editprofile/',views.editprofile,name='editprofile'),
]