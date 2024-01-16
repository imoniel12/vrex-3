# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django import forms
import datetime



class CustomUser(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    middle_name = models.CharField(_("middle name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    GENDER_CHOICES = [
        ('', 'Choose Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    sex = models.CharField(_("sex"), max_length=10, choices=GENDER_CHOICES, blank=True)
    USER_TYPE_CHOICES = [
        ('', 'Choose User Type'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    user_type = models.CharField(_("user type"), max_length=10, choices=USER_TYPE_CHOICES, blank=True)
    home_address = models.CharField(_("home address"), max_length=150, blank=True)
    contact_number = models.CharField(
        _("contact number"),
        max_length=150,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+63\d{10}$',
                message=_("Enter a valid cellphone number starting with +63."),
            ),
        ],
        help_text=_("Enter a valid cellphone number starting with +63."),
    )

    def __str__(self):
        return self.username


class SchoolForm(models.Model):  # Renamed the model to follow PEP 8 conventions
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    middle_name = models.CharField(_("middle name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    USER_TYPE_CHOICES = [
        ('', 'Choose User Type'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    user_type = models.CharField(_("Role"), max_length=10, choices=USER_TYPE_CHOICES, blank=True)
    purpose = models.TextField(_("Purpose of Request"), max_length=150, blank=True)
    requestform = [
        ('', 'What are you requesting?'),
        ('f137', 'F137'),
        ('coe', 'COE'),
    ]
    requestform = models.CharField(_("Forms"), max_length=10, choices=requestform, blank=True)
    request_date = models.DateField(_("Request Date"), default=datetime.date.today)  # Add request_date field
    specialinstructions = models.TextField(_("Special Instructions"), max_length=150, blank=True)
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(_("status"), max_length=10, choices=STATUS_CHOICES, default='Ongoing')
    date_released = models.DateTimeField(_("date released"), blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.requestform}"
    
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.recipient} - {self.timestamp}'