from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import NewAccountForm

# Create your views here.
def new_account(request):
    data = {}
    if request.method == 'GET':
        form = NewAccountForm()
        data['form'] = form
        return render(request, 'accounts/new_account.html', data)
    elif request.method == 'POST':
        form = NewAccountForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('boards:home')
