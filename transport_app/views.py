from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import User, Card, Schedule
import io
import qrcode

def home(request):
    """
    Renders the home page.
    """
    return render(request, 'transport_app/home.html')

def register_view(request):
    """
    Handles user registration and automatically generates a Card with a QR code.
    """
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        role = request.POST.get('role')
        password = request.POST.get('password')
        id_number = request.POST.get('id_number').strip()
        level = request.POST.get('level') if role == 'student' else None
        term = request.POST.get('term') if role == 'student' else None
        contact_information = request.POST.get('contact_information').strip()
        
        if not all([name, email, role, password, id_number, contact_information]):
            messages.error(request, "All fields are required.")
            return redirect('register')
        
        if role == 'student' and not all([level, term]):
            messages.error(request, "Level and Term are required for students.")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('register')

        if User.objects.filter(id_number=id_number).exists():
            messages.error(request, "This ID number is already registered.")
            return redirect('register')
        
        try:
            user = User.objects.create_user(
                email=email, name=name, role=role,
                id_number=id_number, level=level, term=term,
                contact_information=contact_information, password=password
            )
            Card.objects.create(user=user)
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")
            return redirect('register')
    
    return render(request, 'transport_app/register.html')

def login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('profile')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')
    
    return render(request, 'transport_app/login.html')

@login_required
def profile_view(request):
    """
    Displays the logged-in user's profile and QR code.
    """
    user = request.user
    card = getattr(user, 'card', None)
    return render(request, 'transport_app/profile.html', {'user': user, 'card': card})

@login_required
def generate_card_view(request):
    """
    Displays the card generation page with user details and QR code.
    """
    user = request.user
    card, created = Card.objects.get_or_create(user=user)
    return render(request, 'transport_app/card_generation.html', {'user': user, 'card': card})

@login_required
def schedule_view(request):
    """
    Displays the latest transport schedule.
    """
    schedules = Schedule.objects.all().order_by('-updated_at')
    return render(request, 'transport_app/schedule.html', {'schedules': schedules})

def staff_info_view(request):
    """
    Lists all staff/faculty with their information.
    """
    staff_members = User.objects.filter(role__in=['staff', 'faculty'])
    return render(request, 'transport_app/staff_info.html', {'staff_members': staff_members})

@login_required
def view_registered_users(request):
    """
    Custom admin view to display all registered users.
    """
    users = User.objects.all()
    return render(request, 'transport_app/admin_users.html', {'users': users})

def logout_view(request):
    """
    Logs out the user and redirects to the login page.
    """
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('login')
    return redirect('home')

def generate_card(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    qr_data = f"UserID: {user.id_number}"
    qr_code_image = qrcode.make(qr_data)
    buffer = io.BytesIO()
    qr_code_image.save(buffer, format="PNG")
    qr_code_base64 = buffer.getvalue()
    
    return render(request, 'transport_app/card_generation.html', {'user': user, 'qr_code': qr_code_base64})
