from django.shortcuts import render,redirect,get_object_or_404
from .forms import SignUpForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import AuthenticationForm
from account.models import User

import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
# Create your views here.

# ..................Signup view function....................

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Account Created Successfully!!')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            request.session["username"] = username
            request.session["email"] = email
            request.session["password"] = password

            send_otp(request)
            return render(request,'user/otp.html',{"email":email})

            # print(username)
            # return redirect('account:login')
        
    else: 
        form = SignUpForm()
    context = {
        'form':form
        }
    return render(request,'user/signup.html',context)


# ..................OTP...........................

def send_otp(request):
    s=""
    for x in range(0,4):
        s+=str(random.randint(0,9))
    request.session["otp"]=s
    send_mail("otp for sign up",s,'rizpahjoseph@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,'user/otp.html')



def  otp_verification(request):
    if  request.method=='POST':
        otp_=request.POST.get("otp")
    if otp_ == request.session["otp"]:
        encryptedpassword=make_password(request.session['password'])
        nameuser=User(username=request.session['username'],email=request.session['email'],password=encryptedpassword)
        nameuser.save()
        messages.info(request,'signed in successfully...')
        User.is_active=True
        return redirect('appmart:index')
    else:
        messages.error(request,"otp doesn't match")
        return render(request,'user/otp.html')



def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Hey, you are already logged in.")
        return redirect("appmart:index")

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
            return redirect("appmart:index")  # Redirect to the desired page after successful login
        else:
            messages.warning(request, 'Email or Password is incorrect.')

    context = {}
    return render(request, 'user/login.html', context)


# .............Logout view function....................

def logoutUser(request):
    logout(request)
    messages.success(request,f'You logged out')
    return redirect('account:login') 

# def index(request):
#     return render(request, 'mart/index.html')