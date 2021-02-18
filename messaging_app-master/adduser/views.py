from django.utils.decorators import decorator_from_middleware
from .middleware import *
from django.contrib.auth import authenticate


@decorator_from_middleware(CreateUserMiddleware)
def create_user_view(request, form):
    if request.method == 'POST':
        try:
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_superuser(email=email, username=username, password=password)
            return redirect('/login/')
        except Exception as e:
            return render(request, 'sign-in.html', {'error': str(e)})
    return render(request, 'sign-in.html')


def login_user_view(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('/')
            else:
                return render(request, 'sign-in.html', {'error': 'User Not Exists'})
        except Exception as e:
            return render(request, 'sign-in.html', {'error': str(e)})
    return render(request, 'sign-in.html')


def logout_user_view(request):
    auth.logout(request)
    return redirect('/login/')
