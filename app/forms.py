from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Client
from django.core.exceptions import ValidationError

# The BusRegisterForm class is a form for registering users with validation that checks if the email
# domain belongs to a student.
class BusRegisterForm(UserCreationForm):
    def clean_email(self):
        """
        This function checks if the email domain belongs to a registered client and raises a validation
        error if it does.
        :return: The email data after checking if the domain is associated with a client in the
        database. If a client is found with the same domain, a validation error is raised.
        """
        data = self.cleaned_data['email']
        for client in Client.objects.all():
            if client.domain in data:
                raise ValidationError("You must register as a student")
        return data

    # This class defines the fields to be included in a form for creating a new user, using the User
    # model.
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']

# This is a Django form class for creating or updating a BusProfile model instance with a single field
# 'domain'.
class BusProfileForm(forms.ModelForm):
    # This is a class that defines the model and fields for a Profile object in Python.
    class Meta:
        model = Profile
        fields = ['domain']

# This is a custom form for user registration that validates the email field against a list of banned
# email domains and addresses.
class UserRegisterForm(UserCreationForm):
    def clean_email(self):
        """
        This function checks if an email is valid and not banned based on the domain and banned list of
        clients.
        :return: The email data after it has been validated and checked against the banned email
        addresses for the associated client domains.
        """
        data = self.cleaned_data['email']
        flag = False
        for client in Client.objects.all():
            if client.domain in data:
                for ban in client.banned.all():
                    if ban.mail in data:
                        raise ValidationError(ban.name + " is not allowed to use Hexagon")
                flag = True
        if not flag:
            raise ValidationError("You must register with a valid mail")
        return data

    # This class defines the fields for a user model including first name, last name, username, email,
    # and two password fields.
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

# This is a Django form class for updating a user profile with an image, bio, and CV file input
# fields, with JavaScript functions for previewing the image and PDF file.
class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'onchange':'previewImg()'
        })
    )

    cv = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept':'application/pdf',
            'onchange':'previewPdf()'
        })
    )

    # This class defines the model and fields for a Profile object.
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'cv']
