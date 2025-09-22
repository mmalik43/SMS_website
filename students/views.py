from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import OTP
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Course, Student

# ----------------------
# Home page
# ----------------------
def home(request):
    return render(request, 'home.html')


    # ----------------- OTP Signup -----------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(username=username, email=email, password=password)
        otp_obj = OTP.objects.create(user=user)
        otp_code = otp_obj.generate_otp()

        # Send OTP via email
        send_mail(
            "Your OTP Code",
            f"Hello {username}, your OTP is {otp_code}",
            "your_email@gmail.com",  # <-- use EMAIL_HOST_USER from settings.py
            [email],
        )

        request.session["otp_user"] = user.id
        return redirect("verify_otp")

    return render(request, "signup.html")



# ----------------------
# Signup view
# ----------------------
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            return redirect('dashboard')
        else:
            messages.error(request, "Signup failed. Please check the form.")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# ----------------------
# Login view
# ----------------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Login failed. Check your username and password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# ----------------------
# Logout view
# ----------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# ----------------------
# Forms
# ----------------------
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'teacher', 'duration',
                  'price', 'starting_date', 'phone_number', 'image']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'roll_number', 'course']


# ----------------------
# Dashboard view (requires login)
# ----------------------
@login_required(login_url='login')
def dashboard(request):
    courses = Course.objects.all()
    students = Student.objects.all()

    # Handle Course Form
    if request.method == "POST" and 'add_course' in request.POST:
        course_form = CourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            course_form.save()
            return redirect('dashboard')
    else:
        course_form = CourseForm()

    # Handle Student Form
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


# ----------------------
# Add / Edit / Delete Course
# ----------------------
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


# ----------------------
# Delete Student
# ----------------------
@login_required(login_url='login')
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('dashboard')
