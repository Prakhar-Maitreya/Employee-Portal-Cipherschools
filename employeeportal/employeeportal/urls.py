from django.contrib import admin
from django.urls import path
from records import views
from django.contrib.auth.views import LogoutView
from records.views import profile_view
from records.views import department_list, delete_department



urlpatterns = [
    path('admin/', admin.site.urls),

    # Public pages
    path('', views.user_login, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Protected (login required) pages
    path('profile/', views.employee_profile, name='employee_profile'),
    path('employees/', views.employee_list, name='employee_list'),
    path('add/', views.add_employee, name='add_employee'),
    path('add-department/', views.add_department, name='add_department'),
    path('delete-employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path('edit-employee/<int:id>/', views.edit_employee, name='edit_employee'),
    path('profile/', profile_view, name='profile'),
    path('delete-department/<int:id>/', delete_department, name='delete_department'),
    path('departments/', department_list, name='department_list'),
]
