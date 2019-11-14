from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView

from .forms import EditAccountForm

# Create your views here.
@login_required(login_url='/login/')
def account_details(request):
    return render(request, 'profile_page.html')

@login_required(login_url='/login/')
def account_delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        return render(request, 'deleted_user.html')
    else:
        return render(request, 'profile_page.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def account_edit(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('accounts:account_details')
    else:
        form = EditAccountForm(instance=request.user)
        args = {'form':form}
        return render(request, 'edit_profile.html',args)
