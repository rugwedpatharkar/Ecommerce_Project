from cmath import log
from tkinter import E
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect,HttpResponse
from .models import Profile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserPasswordChangeForm, ProfileForm, AddressForm
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
import random
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator



def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = authenticate(username=email, password=password)

        if user_obj:
            if user_obj.profile.is_email_verified:
                login(request, user_obj)
                return redirect('/')
            else:
                messages.info(request, 'Your account is not verified.')
        else:
            messages.warning(request, 'Invalid credentials')

    return render(request, 'accounts/login.html')




def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        if password != password_confirmation:
            messages.warning(request, 'Passwords do not match.')
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.filter(username=email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent to your email address.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')




def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        if user.is_email_verified:
            messages.info(request, 'Your email is already verified. Proceed to login.')
        else:
            user.is_email_verified = True
            user.save()
            messages.success(request, 'Your email has been verified, and your account is activated. Proceed to login.')
        return redirect('accounts:login')  # Update the login URL as needed
    except Profile.DoesNotExist:
        return HttpResponse('Invalid Email token')
    
    
    
    
def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')  # Make sure this redirects to the appropriate page




@login_required
def profile_section(request):
    user = request.user
    password_change_form = UserPasswordChangeForm(request.user)

    return render(request, 'accounts/profile_section.html', {
        'user': user,
        'password_change_form': password_change_form,
    })




@login_required
def profile_update(request):
    user = request.user

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        contact_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if profile_form.is_valid() and contact_form.is_valid():
            profile_form.save()
            contact_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile_update')
    else:
        profile_form = UserProfileForm(instance=user)
        contact_form = ProfileForm(instance=user.profile)

    return render(request, 'accounts/profile_update.html', {
        'profile_form': profile_form,
        'contact_form': contact_form,
    })
    
    
    
    
@login_required
def add_address(request):
    user = request.user

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.profile = user.profile
            address.save()
            messages.success(request, 'Address added successfully.')
        else:
            messages.error(request, 'Invalid address form submission.')

    else:
        address_form = AddressForm()

    # Get the list of addresses associated with the user
    addresses = user.profile.addresses.all()

    # Handle address deletion
    addresses_to_delete = request.POST.getlist('addresses_to_delete')
    if addresses_to_delete:
        user.profile.addresses.filter(id__in=addresses_to_delete).delete()
        messages.success(request, 'Selected addresses deleted successfully.')

    return render(request, 'accounts/add_address.html', {
        'user': user,
        'address_form': address_form,
        'addresses': addresses,
    })
    
    
    
    
    
@login_required
def password_update(request):
    user = request.user

    if request.method == 'POST':
        password_form = UserPasswordChangeForm(user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important for maintaining the user's session
            messages.success(request, 'Password updated successfully.')
            return redirect('accounts:password_update')
    else:
        password_form = UserPasswordChangeForm(user)

    return render(request, 'accounts/password_update.html', {
        'password_form': password_form,
    })
    
    
    
    

def send_otp_email(email, otp):
    subject = 'Password Reset OTP - GadgetGalaxy'
    message = f'Your OTP for password reset is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)




def generate_otp():
    return str(random.randint(100000, 999999))





def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        user = User.objects.filter(email=email).first()

        if user:
            otp = generate_otp()
            send_otp_email(email, otp)
            request.session['reset_email'] = email
            request.session['reset_otp'] = otp
            return redirect('accounts:verify_otp')

        messages.warning(request, 'User with this email does not exist.')

    return render(request, 'accounts/forget_password.html')





def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('reset_otp')

        if entered_otp == stored_otp:
            return redirect('accounts:new_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'accounts/verify_otp.html')






@sensitive_post_parameters()
def new_password(request):
    # Check if the session variables are set
    if 'reset_email' not in request.session or 'reset_otp' not in request.session:
        return redirect('accounts:forget_password')

    if request.method == 'POST':
        email = request.session['reset_email']
        password = request.POST.get('new_password1')  # Use the correct field name

        # Get the user using the email
        user = User.objects.filter(email=email).first()

        if user:
            # Set the password
            user.set_password(password)
            user.save()

            # Authenticate the user
            authenticated_user = authenticate(request, username=user.username, password=password)

            if authenticated_user:
                # Log in the user
                login(request, authenticated_user)

                messages.success(request, 'Password reset successfully.')

                # Clear session data
                del request.session['reset_email']
                del request.session['reset_otp']

                return redirect('accounts:login')

        messages.error(request, 'Invalid user. Please try again.')

    return render(request, 'accounts/new_password.html')