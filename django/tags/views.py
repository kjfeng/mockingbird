from django.shortcuts import render
from django.shortcuts import redirect
from onboard.models import Profile
from .forms import TagForm

# Create your views here.
def tags_view(request):
  if request.method == 'POST':
    my_profile = Profile.objects.filter(pk=request.user.id)
    # create a form instance and populate it with data from the request:
    form = TagForm(request.POST)

    # check whether it's valid:
    if form.is_valid():
      # process the data in form.cleaned_data as required
      industries = form.cleaned_data["industry"]
      industry_str = ', '.join(industries)
      my_profile.update(industry=industry_str)
      my_profile.update(onboard_confirmed=True)
      return redirect('home')
    #
    # else:
    #   return render(request, 'tagging/selecttags.html', {'form': form,
    #   'error_message': "You must select at least one industry",
    #   })

  else:
    form = TagForm()
  return render(request, "tagging/selecttags.html", {'form': form, 'error_message':''})
