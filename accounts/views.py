from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from .forms import CreateUserForm, LoginForm
from django.views.generic import View
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# User Signup View
class SignUpView(generic.CreateView):
    form_class = CreateUserForm
    # Goto login on signup
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

# User Login View
class LoginView(View):
    # Handle post request
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        # Existing User Check
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return render(request, 'subscriptions/home.html')
            else:
                return HttpResponse('Inactive user.')
        else:
            return HttpResponseRedirect('signup')
        
        # return render(request, 'subscriptions/home.html')

    # Handle GET request if user signup even when one is already logged in
    def get(self, request):
        if request.user.is_authenticated:
            error = str('Already logged in, logout of the current' + 
            ' user to log into a newly created or another user!')
            return render(request, 'subscriptions/home.html', 
            {'error':error})
        else:
            form_class = LoginForm()
            return render(request, 'accounts/login.html',
            {'form': form_class})

# User Logout View
class LogoutView(View):
    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        auth.logout(request)
        return HttpResponseRedirect('login')

