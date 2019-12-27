from django.shortcuts import render
from django.shortcuts import redirect

from onboard.models import Profile, ERROR_MESSAGES
from .forms import TagForm

# Create your views here.
def tags_view(request):
  if request.method == 'POST':
    my_profile = Profile.objects.filter(pk=request.user.id)
    # create a form instance and populate it with data from the request:
    form = TagForm(request.POST, instance=request.user.profile)
    isValidReturn = form.is_valid()
    # check whether it's valid:
    if isValidReturn == 1:
      # process the data in form.cleaned_data as required
      #industries = form.cleaned_data["industry"]
      #industry_str = ', '.join(industries)
      #my_profile.update(industry=industry_str)
      request.user.profile.onboard_confirmed = True
      #my_profile.update(onboard_confirmed=True)
      form.save()
      return redirect('home')
    else:
      error_message = 'You can\'t fly just yet! ' + ERROR_MESSAGES[isValidReturn]
      return render(request, "tagging/selecttags.html", {'form': form, 'error_message': error_message})
    #
    # else:
    #   return render(request, 'tagging/selecttags.html', {'form': form,
    #   'error_message': "You must select at least one industry",
    #   })

  else:
    form = TagForm()
  return render(request, "tagging/selecttags.html", {'form': form, 'error_message':''})
