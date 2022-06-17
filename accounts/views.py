from django.contrib.auth import logout, authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import RegisterForm, LoginForm


def register(request):
    if request.method == 'POST':  # 정보를 입력하고 POST로 넘겼을 때
        form = RegisterForm(request.POST)
        if form.is_valid():
            profile = form.save()
            return render(request, 'accounts/register_done.html', {'profile': profile})
    else:  # 처음 빈 폼 화면
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get(REDIRECT_FIELD_NAME) or 'bookmark:list')
        else:
            return render(request, 'accounts/login_fail.html')
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


@login_required
def my_logout(request):
    logout(request)
    return redirect('bookmark:list')
