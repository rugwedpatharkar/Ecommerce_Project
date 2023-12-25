from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import Profile, Address
from django.contrib.auth.models import User


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserPasswordChangeForm(PasswordChangeForm):
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("New Passwords do not match.")
        return cleaned_data


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['contact_number', 'profile_image']
