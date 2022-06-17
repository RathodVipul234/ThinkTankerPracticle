from django import forms
from users.models import User,PersonalDetails

from django.core.exceptions import ValidationError

class UserProfileForm(forms.ModelForm):
    """
        - User registration form
    """
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "mobile_no",
            "date_of_birth",
        )

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                    'required': True
                }
            )
            if field == 'date_of_birth':
                self.fields[field].widget.input_type="date"


class PersonalDetailsForm(forms.ModelForm):
    """
        - Preonal Detils form will be used for saveing data of hobbies anf age
    """
    class Meta:
        model = PersonalDetails
        fields = ("hobbies",)

    def __init__(self, *args, **kwargs):
        super(PersonalDetailsForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )


class UserLoginForm(forms.Form):
    """
        Used to manage custom Login form view
    """

    email = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': 'form-control',
                }
            )

    def clean(self):
        """
            - clean method will be validate fileds 
        """
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            if not User.objects.filter(
                email=email
            ).exists():
                raise ValidationError("User does not exist with this email")

            user_obj = User.objects.get(
                email=email
            )
            if not user_obj.check_password(password):
                raise ValidationError("Invalid password for this email.")
            if not user_obj.is_active:
                raise ValidationError("User is not active.")
            return user_obj
        return self.cleaned_data