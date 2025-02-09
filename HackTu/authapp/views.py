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
            return redirect("/auth/signup/")
        try:
            if User.objects.get(username = email):
                messages.info(request, "Email Already Registered")
                return render(request, "/auth/signin/")
        except Exception as identifier:
            pass
        
        user = User.objects.create_user(username = email, email = email, password = password)
        user.first_name = fname
        user.last_name = lname
        user.is_active = False
        user.save()
        
        email_subject = f"Activate Your Account {fname}"
        message = render_to_string(
            "activate.html", {
            "user" : user,
            "domain": "127.0.0.1:8000",
            "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
            "token" : generate_token.make_token(user),
        },)
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.send()
        messages.success(
            request, f"Activate Your Account following the link Send to your {email}"
        )
        return redirect("/auth/signin/")
    return render(request, "signup.html")

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
            return redirect("/auth/signin")
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
            return render(request, "signin.html")
    return render(request, "signin.html")

def handlelogout(request):
    logout(request)
    messages.info(request, "Logout Successfully")
    return render(request, "signin.html")

class RequestResetEmailView(View):
    def get(self, request):
        return render(request, "request-reset-email.html")

    def post(self, request):
        email = request.POST.get("email")
        user = User.objects.filter(email=email)

        if user.exists():
            email_subject = "Password Reset"
            message = render_to_string(
                "reset-user-password.html",
                {
                    "domain": "127.0.0.1:8000",
                    "uid": urlsafe_base64_encode(force_bytes(user[0].pk)),
                    "token": PasswordResetTokenGenerator().make_token(user[0]),
                },
            )

            # email_message = EmailMessage(
            #     email_subject, message, settings.EMAIL_HOST_USER, [email]
            # )
            # email_message.send()

            messages.info(
                request,
                f"WE HAVE SENT YOU AN EMAIL WITH INSTRUCTIONS ON HOW TO RESET THE PASSWORD {message}",
            )
            return render(request, "request-reset-email.html")

        else:
            messages.error(request, "Invalid Email")
            return render(request, "request-reset-email.html")


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {"uidb64": uidb64, "token": token}
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, "Password Link is Invalid")
                return render(request, "request-reset-email.html")

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request, "set-new-password.html", context)

    def post(self, request, uidb64, token):
        context = {"uidb64": uidb64, "token": token}
        password = request.POST["pass1"]
        connfirm_password = request.POST["pass2"]
        if connfirm_password != password:
            messages.warning(request, "Please Check your Password")
            return render(request, "set-new-password.html", context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password Reset Successfully")
            return redirect("/auth/login")

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "Something Went Wrong, Try Again Later")
            return render(request, "/auth/login")

        return render(request, "set-new-password.html", context)
