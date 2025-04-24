from django.urls import path

from . import views

app_name = 'diaries'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('write', views.write, name='write'),
    path('logout', views.logout, name='logout'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('edit/<int:entry_id>', views.edit, name='edit'),
    path('csrftest', views.csrftest, name='csrf')  
]