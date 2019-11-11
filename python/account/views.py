from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView

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

# Create your models here.
class account_update(UpdateView):
    model = User.profile
    fields = ['email']