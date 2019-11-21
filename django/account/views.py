from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import sys


from .forms import EditAccountForm, EditProfileForm

# Create your views here.
@login_required(login_url='/login/')
def account_details(request):
    return render(request, 'account/profile_page.html')

@login_required(login_url='/login/')
def account_delete(request):
    # print(request)
    # if request.method == 'POST':
    request.user.delete()
    return render(request, 'account/deleted_user.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def account_edit(request):
    initial_data = {
        'year_in_school': request.user.profile.year_in_school,
        'industry': request.user.profile.industry,
        'major': request.user.profile.major,
        'role': request.user.profile.role
    }
    obj = request.user.profile
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        formB = EditProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid() and formB.is_valid():
            form.save()
            formB.save()
            return redirect('account:account_details')
    else:
        form = EditAccountForm(instance=request.user)
        formB = EditProfileForm(instance=request.user.profile, initial=initial_data)
        args = {'form': form, 'formB': formB}
        return render(request, 'account/edit_profile.html', args)


@login_required(login_url='/login')
def change_password(request):
    print("here", file=sys.stderr)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account:account_details')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = PasswordChangeForm(instance=request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })