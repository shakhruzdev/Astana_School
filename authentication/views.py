from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from .forms import UserEditForm
from blog.models import Category, Post
from .models import Student, Teacher
from django.contrib.auth import get_user_model

User = get_user_model()


def register_view(request):
    if request.method == "POST":
        role = request.POST.get("role")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")

        if password != password_confirmation:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if role == "teacher":
            teacher_code = request.POST.get("teacher_code")
            if teacher_code != settings.TEACHER_SECRET_CODE:
                messages.error(request, "Incorrect teacher code.")
                return redirect("register")

        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        middle_name = request.POST.get("middle_name")
        gender = request.POST.get("gender")
        birth_date = request.POST.get("birth_date")
        profile_picture = request.FILES.get("profile_picture")

        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            gender=gender,
            birth_date=birth_date,
            profile_picture=profile_picture,
            role=role,
            password=password,
        )
        user.save()

        if role == "student":
            grade = request.POST.get("grade")
            Student.objects.create(user=user, grade=grade)
        elif role == "teacher":
            subject = request.POST.get("subject")
            work_experience = request.POST.get("work_experience")
            Teacher.objects.create(user=user, subject=subject, work_experience=work_experience)

        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Incorrect email or password')
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def profile_view(request):
    user = request.user
    profile = None

    if user.role == "teacher":
        profile = Teacher.objects.get(user=user)
    elif user.role == "student":
        profile = Student.objects.get(user=user)

    context = {
        'user': user,
        'profile': profile
    }

    return render(request, 'profile.html', context)


def home_view(request):
    posts = Post.objects.order_by("?")[:2]
    teachers = Teacher.objects.order_by("?")[:3]

    context = {
        'posts': posts,
        'teachers': teachers
    }

    return render(request, 'index-login.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
