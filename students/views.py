from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from .models import Course, Student

# Home page
def home(request):
    return render(request, 'home.html')



# Signup view (no OTP)

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Password match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # Username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("signup")

        # Email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, "Signup successful! You are now logged in.")
        return redirect("dashboard")

    return render(request, "signup.html")



# Login view

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")


# Logout view

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")



# Forms
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'teacher', 'duration',
                  'price', 'starting_date', 'phone_number', 'image']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'roll_number', 'course']



# Dashboard

@login_required(login_url='login')
def dashboard(request):
    courses = Course.objects.all()
    students = Student.objects.all()

    # Handle Course form submission
    if request.method == "POST" and 'add_course' in request.POST:
        course_form = CourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            course_form.save()
            return redirect('dashboard')
    else:
        course_form = CourseForm()

    # Handle Student form submission
    if request.method == "POST" and 'add_student' in request.POST:
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student_form.save()
            return redirect('dashboard')
    else:
        student_form = StudentForm()

    context = {
        'courses': courses,
        'students': students,
        'form': course_form,
        'student_form': student_form,
    }
    return render(request, 'dashboard.html', context)



# Add/Edit/Delete Course

@login_required(login_url='login')
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form, 'title': 'Add Course'})


@login_required(login_url='login')
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form, 'course': course})


@login_required(login_url='login')
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('dashboard')


# Delete Student

@login_required(login_url='login')
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('dashboard')
