from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    pass
#
# class SignUpForm(forms.ModelForm):
#     password1 = forms.CharField(
#         label=helpers("Password"),
#         strip=False,
#         widget=forms.PasswordInput,
#         max_length=254,
#         min_length=2,
#     )
#
#     password2 = forms.CharField(
#         label=helpers("Password confirmation"),
#         widget=forms.PasswordInput,
#         strip=False,
#         help_text=helpers("Enter the same password as before, for verification."),
#     )
#
#     class Meta:
#
#         model = User
#         fields = ("email",)
#
#     def __init__(self, *args, **kwargs):
#
#         super().__init__(*args, **kwargs)
#
#     def clean_password2(self):
#
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 helpers("Passwords given do not match."))
#         return password2
#
#     def clean_email(self):
#
#         data = self.cleaned_data['email']
#         if User.objects.filter(email=data).exists():
#             raise forms.ValidationError("This email is already being used.")
#         return data
#

class LogoutForm(forms.Form):
    pass



class EditProfile(forms.Form):

    email = forms.CharField(label='Email', max_length=100)
    first_name = forms.CharField(label='First Name', max_length=100)

    def __init__(self, user=None,  *args, **kwargs):

        self.user = user

        super(EditProfile, self).__init__(*args, **kwargs)


    def save(self):

        if not self.user:
            raise forms.ValidationError("User needs to be specified to save profile")

        self.user.email = self.cleaned_data['email']
        self.user.first_name = self.cleaned_data['first_name']
        self.user.save()

        return self.user

    def clean_email(self):

        data = self.cleaned_data['email']
        email = User.objects.exclude(pk=self.user.pk).filter(email=data)

        if email.exists():
            raise forms.ValidationError("This email is already being used.")

        return data


class LoginForm(forms.Form):

    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput)
