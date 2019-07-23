from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin', admin.site.urls),
    path('',views.index, name='index'),
    path('post/<int:post_id>', views.detail, name = 'detail'),
    path('new',views.new, name='new'), 
    path('create',views.create, name="create"),
    path('<int:post_id>/update', views.update, name='update'), 
    path('<int:post_id>/modify', views.modify, name='modify'),
    path('<int:post_id>/delete', views.delete , name="delete"),
    path('newpost', views.newpost,name="newpost"),
    path('<int:post_id>/upadatemodify', views.updatemodify , name="updatemodify"),
    path('<int:post_id>/comment_new', views.comment_write, name="comment_write"),    
]
