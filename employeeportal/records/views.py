from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Department, Role
from .forms import EmployeeForm, CustomSignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import DepartmentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


@login_required
def employee_list(request):
    dept_id = request.GET.get('department')
    employees = Employee.objects.all()
    if dept_id:
        employees = employees.filter(department__id=dept_id)

    departments = Department.objects.all()
    return render(request, 'employee_list.html', {'employees': employees, 'departments': departments})


@login_required
def add_employee(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission.")

    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'add_employee.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('employee_list')  # already logged in

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('employee_list')  # redirect after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def employee_profile(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None

    return render(request, 'employee_profile.html', {'employee': employee})


@login_required
def add_department(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission.")
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'add_department.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone_number')

            # Assign role
            role_name = 'Admin' if user.is_superuser else 'Employee'
            role, _ = Role.objects.get_or_create(name=role_name)

            # Create linked Employee
            Employee.objects.create(
                user=user,
                name=user.username,
                email=email,
                phone_number=phone,
                role=role
            )
            return redirect('login')
    else:
        form = CustomSignupForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def delete_employee(request, id):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('employee_list')

    employee = get_object_or_404(Employee, pk=id)
    user = employee.user
    recipient_email = employee.email
    employee_name = employee.name

    send_mail(
        subject="Employment Terminated",
        message=f"Hello {employee_name},\n\nYour employee record has been removed from the system.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )

    employee.delete()
    user.delete()

    messages.success(request, f"Employee '{employee_name}' and their user account have been deleted.")
    return redirect('employee_list')


@login_required
def delete_department(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admins can delete departments.")

    dept = get_object_or_404(Department, id=id)
    affected_employees = Employee.objects.filter(department=dept)

    for employee in affected_employees:
        recipient_email = employee.email
        employee_name = employee.name
        user = employee.user

        send_mail(
            subject="Department Deleted",
            message=f"Dear {employee_name},\n\nYour department '{dept.name}' has been removed from the system. As a "
                    f"result, your employee record has also been deleted.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )

        employee.delete()
        if user:
            user.delete()

    dept_name = dept.name
    dept.delete()

    messages.success(request, f"Department '{dept_name}' and its employees were deleted.")
    return redirect('employee_list')


@login_required
@login_required
def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if not request.user.is_superuser and employee.user != request.user:
        return HttpResponseForbidden("You do not have permission to edit this employee.")

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'edit_employee.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def department_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admins can view this page.")
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})
