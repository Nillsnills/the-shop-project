from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'register successful')
            return redirect('homepage')

        else:
            messages.error(request, 'registration failed')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, "UserRegister.html", context)
