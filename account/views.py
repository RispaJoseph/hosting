from django.shortcuts import render,redirect,get_object_or_404
from .forms import SignUpForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import AuthenticationForm
from account.models import User
# Create your views here.

# ..................Signup view function....................

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Account Created Successfully!!')
            form.save()
            username = form.cleaned_data.get('username')
            print(username)
            return redirect('account:login')
    else: 
        form = SignUpForm()
    context = {
        'form':form
        }
    return render(request,'user/signup.html',context)


# .............Login view function....................

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return None

#         if user.check_password(password):
#             return user
#         return None

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Hey, you are already logged in.")
        return redirect("account:index")

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)

        user = get_object_or_404(User, email=email)
        # user=User.objects.get(email=email)
        user = authenticate(request, email=email, password=password)
        print (user)

        if user is not None:
            login(request, user)
            request.session['logged_in'] = True  # Set a session variable if needed
            messages.success(request, 'Login successful.')
            return redirect("account:index")  # Redirect to the desired page after successful login
        else:
            messages.warning(request, 'Email or Password is incorrect.')

    context = {}
    return render(request, 'user/login.html', context)


# .............Logout view function....................

def logoutUser(request):
    logout(request)
    messages.success(request,f'You logged out')
    return redirect('account:login') 

def index(request):
    return render(request, 'mart/index.html')