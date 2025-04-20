from django.urls import path
from . import views


urlpatterns = [
    path('', views.home), 
    path('home',views.home),
    path('register',views.register),
    path('login',views.login),
    path('adminhome',views.adminhome),
    path('predict/', views.predict), 
    path('add_bird_species',views.bird_species),
    path('click',views.viewbird),
    path('addtips',views.addtips),
    path('viewuser',views.viewuser),
    path('qsbank',views.qsbank),
    path('viewsug',views.view_suggestion),
    path('logout', views.login), 
    # USER
    path('userhome',views.userhome),
    path('v_species',views.v_species),
    path('v_tips',views.v_tips),
    path('v_qst',views.v_qst),
    path('add_sug',views.add_sug),
    path('predict/', views.predict), 
    path('analysedata/', views.analysedata), 
    path('edit_user',views.edit_user),
    path('delete_user',views.delete_user),
    path('del_sou',views.del_sou)


    #path('analysedata/', views.analysedata), 
]
