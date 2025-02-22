from django import forms
from django.core.exceptions import ValidationError
from users.models import User


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, widget=forms.TextInput(
        attrs={"placeholder": "Username(more than 3 characters)"}
    ))
    password = forms.CharField(min_length=4, widget=forms.PasswordInput(
        attrs={"placeholder": "Password(more than 4 characters)"}
    ))


class SignupForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    profile_image = forms.ImageField()  # 값은 옵션값이다. 어떻게 정의하지?
    short_description = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"{username} is already exists")
        return username

    def clean(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            self.add_error("password2", "Passwords don't match")

    def save(self):
        username = self.cleaned_data['username']
        password1 = self.cleaned_data['password1']
        profile_image = self.cleaned_data['profile_image']
        short_description = self.cleaned_data['short_description']

        user = User.objects.create_user(
            username=username,
            password=password1,
            profile_image=profile_image,
            short_description=short_description,
        )

        return user
