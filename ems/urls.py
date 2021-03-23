from django.urls import path

from ems import views

app_name = 'ems'

urlpatterns = [
    path("index/", views.index, name='index'),
    path("del_s/", views.del_session, name='del_s'),
    path("del/", views.deluser, name='del'),
    path("add/", views.adduser, name='add'),
    path("add2/", views.adduser2, name='add2'),
    path("update/", views.updateuser, name='update'),
    path("update2/", views.updateuser2, name='update2'),
]
