from django.shortcuts import render, redirect
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from .forms import EditAccountForm, EditProfileForm

# Create your views here.
@login_required(login_url='/login/')
def account_details(request):
    return render(request, 'account/profile_page.html')

@login_required(login_url='/login/')
def account_delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        return render(request, 'account/deleted_user.html')
    else:
        return render(request, 'account/profile_page.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def account_edit(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        formB = EditProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid() and formB.is_valid():
            form.save()
            formB.save()
            return redirect('account:account_details')
    else:
        form = EditAccountForm(instance=request.user)
        formB = EditProfileForm(instance=request.user)
        args = {'form': form, 'formB': formB}
        return render(request, 'account/edit_profile.html', args)

@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('account:account_details'))
        else:
            return redirect(reverse('account:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'account/change_password.html', args)