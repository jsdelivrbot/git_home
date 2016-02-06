from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.models import User

from .forms import signup_form

def index(request):
    form = signup_form()
    return render(request, "main/index.html", {"form": form})

def signup(request):
    if request.method == 'POST':
        form = signup_form(request.POST)
    if form.is_valid():
        username = form.username
        email = form.email
        password = form.password
        confirm_password = form.confirm_password
        if password != confirm_password:
            return HttpResponseRedirect(reverse("main:index"))
        else:
            user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password)

            return HttpResponseRedirect(reverse("main:index"))
