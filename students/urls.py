from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-course/', views.add_course, name='add_course'),
    path('edit-course/<int:pk>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:pk>/', views.delete_course, name='delete_course'),
    path('delete-student/<int:pk>/', views.delete_student, name='delete_student'),

]
