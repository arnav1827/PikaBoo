from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# for generating tokens

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import TokenGenerator, generate_token
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def register(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")
        if confirm_password != password:
            messages.warning(request, "Please enter correct Password")
            return redirect("/auth/register/")
        try:
            if User.objects.get(username = email):
                messages.info(request, "Email Already Registered")
                return render(request, "/auth/login/")
        except Exception as identifier:
            pass
        
        user = User.objects.create_user(username = email, email = email, password = password)
        user.first_name = fname
        user.last_name = lname
        user.is_active = False
        user.save()
        
        email_subject = f"Activate Your Account {fname}"
        message = render_to_string("activate.html"{
            "user":user,
            "domain": 127.0.0.1:8000,
            "uid" : urlsafe_base64_encode(force_byte(user.pk)),
            "token" : generate_token.make_token(user),
        },)
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.send()
        messages.success(
            request, f"Activate Your Account following the link Send to your {email}"
        )
        return redirect("/auth/login/")
    return render(request, "register.html")

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
        except:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account Activate Successfully !")
            return redirect("/auth/login")
        return render(request, "activationfail.html")
    
def handlelogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        userpassword = request.POST.get("password")
        myuser = authenticate(email = email, password = userpassword)
        if myuser is not None:
            login(request, myuser)
            messages.info(request, "Login Successfully")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, "login.html")
    return render(request, "login.html")

def handlelogout(request):
    logout(request)
    messages.info(request, "Logout Successfully")
    return render(request, "login.html")
