from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import RegistrationForm
from .models import Profile, Contact
from django.http import HttpResponse, JsonResponse


@login_required
def dashboard(request):
    return render(
        request,
        'account/dashboard.html',
    )


def profile_detail(request, profile_slug):
    user_profile = get_object_or_404(Profile, slug=profile_slug)
    users_contact = None
    if user_profile.user != request.user:
        try:
            users_contact = Contact.objects.get(user_from=request.user, user_to=user_profile.user)
        except:
            users_contact = None
    return render(
        request,
        'account/profile.html',
        {
            'user_profile': user_profile,
            'users_contact': users_contact
        }
    )


@require_POST
def follow(request):
    user_to = User.objects.get(pk=int(request.POST.get('id')))
    action = request.POST.get('action')

    if user_to and action:
        user_contact, created = Contact.objects.get_or_create(user_from=request.user, user_to=user_to)
        if action == 'follow':
            user_contact.save()
        elif action == 'unfollow':
            user_contact.delete()
        else:
            JsonResponse({'status': 'error'})
    else:
        JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'ok'})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            cd = form.cleaned_data
            new_user.set_password(cd['password'])
            new_user.save()
            Profile(user=new_user, profile_name=cd['username'], email=cd['email']).save()
            return render(
                request,
                'account/register_done.html',
            )
    else:
        form = RegistrationForm()
        return render(
            request,
            'account/register.html',
            {
                'form': form,
            }
        )


@require_POST
def get_csrf(request):
    print(request.POST.get('file'))
    return HttpResponse('okk')
