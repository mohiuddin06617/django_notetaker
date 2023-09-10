from django import forms
from django.core.exceptions import ValidationError

from accounts.validators import validate_full_name, validate_username
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=50,
        min_length=3,
        widget=forms.TextInput(
            attrs={"class": "form-control", "autocomplete": "given-name"}
        ),
        strip=True,
        help_text="Full Name should contain only Latin letters, and should include no more than 3 words",
    )

    class Meta:
        model = User
        fields = ("full_name", "email", "password1", "password2")

    def clean_full_name(self):
        data = self.cleaned_data["full_name"]
        if not data.replace(" ", "").isalpha():
            raise forms.ValidationError("Full Name should contain only Latin letters.")
        if len(data.split()) > 3:
            raise forms.ValidationError("Full Name should include no more than 3 words.")
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "autocomplete": "email"})
        self.fields["password1"].widget.attrs.update({"autocomplete": "new-password", "class": "form-control"})
        self.fields["password2"].widget.attrs.update({"autocomplete": "new-password", "class": "form-control"})


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "full_name")

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "autocomplete": "username"}
            ),
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "autocomplete": "full_name"}
            ),
        }

    def clean_username(self):
        # Ensure the username starts with '@' sign.
        user_email = self.cleaned_data.get("email", "")
        username = user_email.split("@")[0]
        validate_username(username)
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name", "")
        validate_full_name(full_name)
        return full_name.title()


class UserCacheMixin:
    user_cache = None


class LogIn(UserCacheMixin, forms.Form):
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError('You entered an invalid password.')

        return password


class EmailForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError('You entered an invalid email address.')

        if not user.is_active:
            raise ValidationError('This account is not active.')

        self.user_cache = user

        return email


class LoginForm(LogIn, EmailForm):
    @property
    def field_order(self):
        return ['email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "autocomplete": "email"})
        self.fields["password"].widget.attrs.update({"autocomplete": "password", "class": "form-control"})
