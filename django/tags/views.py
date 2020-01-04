from django.shortcuts import render
from django.shortcuts import redirect

from onboard.models import Profile, ERROR_MESSAGES
from .forms import TagForm, BasicForm

# Create your views here.
def tags_view(request):
  if request.method == 'POST':
    my_profile = Profile.objects.filter(pk=request.user.id)
    # create a form instance and populate it with data from the request:
    form = TagForm(request.POST, instance=request.user.profile)
    formB = BasicForm(request.POST, instance=request.user.profile)

    isValidReturn = form.is_valid()
    # check whether it's valid:
    if isValidReturn == 1 and formB.is_valid():
      request.user.profile.onboard_confirmed = True
      form.save()
      formB.save()
      return redirect('home')
    else:
      error_message = 'You can\'t fly just yet! ' + ERROR_MESSAGES[isValidReturn]
      formB.fields['role'].label = "Desired Role"
      formB.fields['summary'].label = "Here's some space to tell us a little more about yourself!"
      formB.fields['summary'].help_text = "Tell us about your career goals or current projects or anything else!" \
                                          "This introduction will be visible to all other users."

      return render(request, "tagging/selecttags.html", {'form': form, 'formB':formB, 'error_message': error_message})
  else:
    form = TagForm()
    formB = BasicForm()
    formB.fields['role'].label = "Desired Role"
    formB.fields['summary'].label = "Here's some space to tell us a little more about yourself!"
    formB.fields['summary'].help_text = "Tell us about your career goals or current projects or anything else!" \
                                        "This introduction will be visible to all other users."

  return render(request, "tagging/selecttags.html", {'form': form, 'formB': formB, 'error_message':''})
