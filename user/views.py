from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not user.is_superuser and not user.is_staff:
                user.is_customer = True
                user.save()

            login(request, user)
            return redirect('homepage')

        else:
            messages.error(request, 'registration failed')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, "UserRegister.html", context)


def logout_custom(request):
    logout(request)
    return redirect('homepage')