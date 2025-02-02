from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import qrcode
from PIL import Image

from io import BytesIO
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


class Schedule(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

@receiver(post_save, sender=Schedule)
def send_schedule_update_notification(sender, instance, **kwargs):
    """Sends email notifications to all users when a schedule is updated."""
    from .models import User  # Import here to avoid circular imports

    subject = f"Schedule Update: {instance.title}"
    message = (
        f"Dear User,\n\nThe transport schedule has been updated:\n"
        f"Title: {instance.title}\n"
        f"Description: {instance.description}\n"
        f"Date: {instance.date}\n"
        f"Time: {instance.time}\n\n"
        f"Please log in to check the latest updates.\n\n"
        f"Best Regards,\nCampus Transport Management Team"
    )

    recipient_list = list(User.objects.values_list('email', flat=True))  # Get all user emails
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)

class UserManager(BaseUserManager):
    def create_user(self, email, name, id_number, contact_information, password=None, role='student', level=None, term=None):
        """Creates and returns a user with the given details."""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            name=name,
            role=role,  # Default role is Student unless specified
            id_number=id_number,
            contact_information=contact_information,
            level=level if role == 'student' else None,
            term=term if role == 'student' else None,
        )
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """Creates and returns a superuser without requiring role, level, or term."""
        user = self.create_user(
            email=email,
            name=name,
            id_number="000000",  # Default ID for admin
            contact_information="Admin User",  # Default contact
            password=password,
            role="admin"  # Admin role assigned automatically
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),  # Add Admin as a Role
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    id_number = models.CharField(max_length=20, unique=True)
    level = models.CharField(max_length=50, null=True, blank=True)  # Optional for non-students
    term = models.CharField(max_length=50, null=True, blank=True)  # Optional for non-students
    contact_information = models.TextField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin


class Card(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.user.id_number:
            raise ValueError("User must have an ID number to generate a QR code.")

        serial_number = self.user.pk
        qr_data = f"SERIAL: {serial_number}, ID: {self.user.id_number}"

        qr = qrcode.make(qr_data)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        file_name = f"qr_code_{serial_number}_{self.user.id_number}.png"

        self.qr_code.save(file_name, File(buffer), save=False)
        super().save(*args, **kwargs)
